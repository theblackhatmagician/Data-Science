Extract Reddit Data using PushShift and PRAW.
PushShift stores the reddit data in third party servers. Although it updates frequently, We won't get the Real time data(Upvotes,Comments,etc.).
PRAW is a wrapper to redditAPI, which won't allow us to fetch data between range, also it is limited to 1000 posts per request.
Thus Using PushShift with PRAW gives the ability to get realtime data between a certain range, and can be used for many sentimental Analysis.
