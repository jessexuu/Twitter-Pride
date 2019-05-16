import pymongo
import json

myclient = pymongo.MongoClient("mongodb://115.146.92.137:30003")
mydb = myclient['harvesting']
raw_col = mydb['rawdata']
filtered_col = mydb['test_filtered']

default_profile_url = 'http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'

cursor = raw_col.find()
for document in cursor:
    user_object = document['user']
    place_object = document['place']
    tweet_created_time = document['created_at']

    profile_url = user_object['profile_image_url']

    if(profile_url != default_profile_url):
        normal_image_url = profile_url
        original_image_url = normal_image_url.replace("_normal","")
        document['user']['profile_image_url'] = original_image_url

        filtered_col.insert_one({
            "user": user_object,
            "place": place_object,
            "tweet_created_time": tweet_created_time
        })

        print("{} user added".format(user_object['id']))
