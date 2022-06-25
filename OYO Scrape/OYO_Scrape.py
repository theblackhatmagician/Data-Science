import requests
import pandas as pd
import json
from pandas import json_normalize
import urllib

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

q = input("Enter Location:")
q = q.replace(" ",'%20')
load = "https://www.oyorooms.com/api/pwa/autocompletenew?query="+q
search = requests.get(load, headers = headers)
search_data = json.loads(search.text)
print(search_data['responseObject'][0]['name'])

loc = search_data['responseObject'][0]['name']+", "+search_data['responseObject'][0]['city']['name']+", "+search_data['responseObject'][0]['state']['name']
lat = search_data['responseObject'][0]['centerPoint']['lat']
log = search_data['responseObject'][0]['centerPoint']['lng']

checkin = '12/03/2022'
checkout = '13/03/2022'

pagepayload =  {'location' : loc, 'latitude' : lat, 'longitude' : log, 'searchType' : 'locality', 'coupon' : '', 'checkin' : checkin, 'checkout' : checkout, 'roomConfig[]' : 2, 'country' : 'india', 'guests' : 2, 'rooms' : 1}
url_encode1 = urllib.parse.urlencode(pagepayload, quote_via=urllib.parse.quote)
url_encode2 = urllib.parse.quote('/search?'+url_encode1,safe='') 
urlfinal = 'https://www.oyorooms.com/api/pwa/getListingPage?url='+url_encode2

listing = requests.get(urlfinal, headers = headers)
listing_data = json.loads(listing.text)
hotels_list = listing_data['searchData']['hotels']
hotel_df = json_normalize(hotels_list)


excel_df = pd.DataFrame()

excel_df['Hotel Name'] = hotel_df['name']
excel_df['Distance'] = hotel_df['distance']
excel_df['Type'] = hotel_df['hotel_type']
excel_df['Image URL'] = hotel_df['best_image']
excel_df['Price'] = json_normalize(hotel_df['mrcData'].apply(lambda x: x[0]))['finalPrice']
excel_df['Available Rooms'] = hotel_df['available_rooms'].apply(lambda x: x[0])
excel_df['Rating'] = hotel_df['ratings.value'].fillna(0).astype(str) + " (" + hotel_df['ratings.count'].fillna(0).astype(int).astype(str) + ")" 
excel_df['Address'] = hotel_df['address']
excel_df['City'] = hotel_df['city']
excel_df['Hotel link'] = 'https://www.oyorooms.com/' + hotel_df['id'] + '/?rooms=1&guests=2&rooms_config=1-2_0'
excel_df['OYO ID'] = hotel_df['oyo_id']
excel_df['Geo Location'] = hotel_df['geo_location']
excel_df['Category'] = hotel_df['category']

 



pageno = 1
listcount = 20

while True:
    
    apiloadmore = 'id,name,city,street,category,geo_location,category,hotel_type,alternate_name,country_name,country_id,short_address,address,hotel_name_without_category,categorywise_images,category_wise_media,category_availability,external_booking_url,status&additional_fields=hotel_badge,category_info,cancellation_policies,best_image,room_pricing,availability,amenities,restrictions,category,captains_info,new_applicable_filters,additional_charge_info,images,hotel_images,collection_filtered_count,popular_location_range,guest_ratings,oyo_wizard,urgency_info,oyo_owner_discount,category_wise_pricing&tax_exclusive_pricing=true&available_room_count[checkin]={cin}&available_room_count[checkout]={cout}&available_room_count[min_count]=1&filters[page]={pgno}&filters[coordinates][latitude]={latitude}&filters[coordinates][longitude]={logitude}&filters[all_room_categories]=true&pre_apply_coupon_switch=true&search_redirection_enabled=true&rooms_config=0,1,0&requested_coupon=&services=meals&source=Web Booking&format_response[batch][count]=20&format_response[batch][offset]={lstcount}&format_response[sort_params][sort_on]=&format_response[sort_params][ascending]=true&locale=en'.format(cin = checkin, cout = checkout, logitude = log, latitude = lat, pgno = pageno, lstcount = listcount)
    loadmoreurl = 'https://www.oyorooms.com/api/pwa/search/hotels?fields=' + urllib.parse.quote(apiloadmore,safe='=&')
    more_listing = requests.get(loadmoreurl, headers = headers)
    more_listing_data = json.loads(more_listing.text)
    more_hotels_list = more_listing_data['hotels']
    more_hotel_df = json_normalize(more_hotels_list)
    
    if 'name' not in more_hotel_df.keys():
        break
    else:
        listcount *= 2
        
        more_excel_df = pd.DataFrame()
        more_excel_df['Hotel Name'] = more_hotel_df['name']
        more_excel_df['Distance'] = more_hotel_df['distance']
        more_excel_df['Type'] = more_hotel_df['hotel_type']
        more_excel_df['Image URL'] = more_hotel_df['best_image']
        more_excel_df['Price'] = json_normalize(more_hotel_df['mrcData'].apply(lambda x: x[0]))['finalPrice']
        more_excel_df['Available Rooms'] = more_hotel_df['available_rooms'].apply(lambda x: x[0])
        more_excel_df['Rating'] = more_hotel_df['ratings.value'].fillna(0).astype(str) + " (" + more_hotel_df['ratings.count'].fillna(0).astype(int).astype(str) + ")" 
        more_excel_df['Address'] = more_hotel_df['address']
        more_excel_df['City'] = more_hotel_df['city']
        more_excel_df['Hotel link'] = 'https://www.oyorooms.com/' + more_hotel_df['id'] + '/?rooms=1&guests=2&rooms_config=1-2_0'
        more_excel_df['OYO ID'] = more_hotel_df['oyo_id']
        more_excel_df['Geo Location'] = more_hotel_df['geo_location']
        more_excel_df['Category'] = more_hotel_df['category']
        
        excel_df = excel_df.append(more_excel_df,ignore_index=True)

print(excel_df)            
excel_style_df = excel_df.style.set_properties(**{'background-color': 'yellow'}, subset=['OYO ID', 'Geo Location'])
excel_style_df.to_excel("oyo_"+search_data['responseObject'][0]['name']+"_scrape.xlsx",sheet_name='OYO_'+search_data['responseObject'][0]['name'])
