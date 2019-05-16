import pymongo
import json

myclient = pymongo.MongoClient("mongodb://115.146.92.137:30003")
mydb = myclient['harvesting']
raw_col = mydb['rawdata']
filtered_col = mydb['test_filtered']

default_profile_url = 'http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
filtered = []

api_url = 'http://115.146.92.137:8000/api/v1/'
detect_api = '{}face_detection'.format(api_url)
compare_api = '{}face_comparison'.format(api_url)

#adds all existing IDs from filtered DB
cursor = filtered_col.find()
for document in cursor:
    user_id = document['user']['id']
    filtered.append(user_id)

#process filtering for new users
cursor = raw_col.find()
for document in cursor:
    user_object = document['user']
    place_object = document['place']
    tweet_created_time = document['created_at']
    user_id = user_object['id']

    duplicate = 0

    #check for duplicates
    for x in range(len(filtered)):
        if(filtered[x] == user_id):
            duplicate = 1
            print('dup found')
            break

    if(duplicate == 0):
        profile_url = user_object['profile_image_url']
        #ignore profiles with no profile image
        if(profile_url != default_profile_url):
            normal_image_url = profile_url
            original_image_url = normal_image_url.replace("_normal","")
            document['user']['profile_image_url'] = original_image_url

            #insert into filtereed DB
            filtered_col.insert_one({
                "user": user_object,
                "place": place_object,
                "tweet_created_time": tweet_created_time
            })
            print("insert done")
