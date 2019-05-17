%python

import pymongo
import json
import requests
from io import BytesIO
from PIL import Image

#declare variables
myclient = pymongo.MongoClient("mongodb://103.6.254.149:30003")
mydb = myclient['harvesting']
raw_col = mydb['rawdata']
filtered_col = mydb['test_filtered']

default_profile_url = 'http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
filtered = []

api_url = 'http://103.6.254.149:8000/api/v1/'
detect_api = '{}face_detection'.format(api_url)
compare_api = '{}face_comparison'.format(api_url)

detect_limit = 3
face_score_threshold = 0.6

def add_skipped_status(doc_id, reason = "not provided"):

    query_curr_doc = {
        "_id": doc_id
    }

    add_skipped = {
        "$set": {
            "skipped": reason
        }
    }

    raw_col.update_one(query_curr_doc, add_skipped)

#adds all existing IDs from filtered DB
cursor = filtered_col.find()
for document in cursor:
    user_id = document['user']['id']
    filtered.append(user_id)

#process filtering for new users
#skips over docs with skipped field
cursor = raw_col.find({
    "skipped": {"$exists": False}
})
for document in cursor:
    user_object = document['user']
    place_object = document['place']
    user_id = user_object['id']

    duplicate = False

    #check for duplicates
    for x in range(len(filtered)):
        if(filtered[x] == user_id):
            duplicate = True
            print('dup found')
            add_skipped_status(document['_id'], "duplicate user")
            break

    if(duplicate == False):
        profile_url = user_object['profile_image_url']
        #ignore profiles with no profile image
        if(profile_url == default_profile_url):
            print("default pp")
            add_skipped_status(document['_id'], "no profile picture")
        else:
            #obtain original image url
            normal_image_url = profile_url
            original_image_url = normal_image_url.replace("_normal","")
            user_object['profile_image_url'] = original_image_url

            #open url as image file
            r = requests.get(original_image_url, stream=True)
            image_file = BytesIO(r.content)

            files = {
                "image_file": image_file
            }

            data = {
                "limit": detect_limit
            }

            #analyse profile picture
            detect_response = requests.post(detect_api, files=files, data=data).json()
            if('scores') not in detect_response:
                print('no scores')
                add_skipped_status("API unable to generate scores")
            else:
                scores = detect_response['scores']
                faces = []
                for x in range(detect_limit):
                    if(scores[x] > face_score_threshold):
                        faces.append({
                            "score": scores[x],
                            "ymin": detect_response['faces'][x][0],
                            "xmin": detect_response['faces'][x][1],
                            "ymax": detect_response['faces'][x][2],
                            "xmax": detect_response['faces'][x][3]
                        })

                # ensure profile picture contains single person
                if(len(faces) < 1):
                    print("no face")
                    add_skipped_status(document['_id'], "no face in profile picture")
                elif(len(faces) > 1):
                    print("more than 1 face")
                    add_skipped_status(document['_id'], "detected multiple face in profile picture")
                else:
                    #crop face from image -- this section is placed after comparison API
                    # follow this https://colab.research.google.com/drive/18OFWCfMR2Iz2EgXsonU7WgDM5UP7vOQq
                    # && https://blog.goodaudience.com/using-the-twitter-api-with-python-c6e8da96d273 for Twitter API
                    # temp = Image.open(image_file)
                    # width, height = temp.size
                    # top = faces[0]['ymin'] * height
                    # left = faces[0]['xmin'] * width
                    # right = faces[0]['xmax'] * width
                    # bottom = faces[0]['ymax'] * height
                    #
                    # cropped = temp.crop((int(left), int(top), int(right), int(bottom)))
                    # new_image = BytesIO()
                    # cropped.save(new_image, format='png')
                    # new_image.seek(0)
                    # image_file.seek(0)

                    #create new document
                    new_user = {
                        "user": user_object,
                        "place": place_object,
                        "face": faces[0]
                        # "profile_img": temp,
                        # "cropped_face": cropped
                    }

                    #insert new document into filtereed DB
                    filtered_col.insert_one(new_user)
                    print("insert done")
