import pymongo
import json
import requests
from PIL import Image
from io import BytesIO

myclient = pymongo.MongoClient("mongodb://115.146.92.137:30003")
mydb = myclient['harvesting']
raw_col = mydb['rawdata']
filtered_col = mydb['test_filtered']

default_profile_url = 'http://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'
filtered = []

api_url = 'http://115.146.92.137:8000/api/v1/'
detect_api = '{}face_detection'.format(api_url)
compare_api = '{}face_comparison'.format(api_url)

detect_limit = 3


img_url = 'https://pbs.twimg.com/profile_images/1126882595814248449/FXjwUAmJ.jpg'

r = requests.get(img_url, stream=True)
image_file = BytesIO(r.content)

files = {
    "image_file": image_file
}

data = {
    "limit": 3,
}

detect_response = requests.post(detect_api, files=files, data=data).json()
faces = detect_response['faces']
print(faces)
# scores = detect_response['scores']
# print(Image.open(image_file).size)

# print(scores)
# highest_score = 0
# for x in range(1,3):
#     if(scores[x] > scores[highest_score]):
#         highest_score = x
#
# face_position = detect_response['faces'][highest_score]
#
# temp = Image.open(image_file)
# width, height = temp.size
#
# top = face_position[0] * height
# left = face_position[1] * width
# right = face_position[3] * width
# bottom = face_position[2] * height
#
# cropped = temp.crop((int(left), int(top), int(right), int(bottom)))
# new_image = BytesIO()
# cropped.save(new_image, format='png')
# new_image.seek(0)
#
# files = {
#     "image_file": new_image
# }
#
# rr = requests.post(detect_api, files=files, data=data).json()
# print(rr)

# #process filtering for new users
# cursor = raw_col.find()
# for document in cursor:
#     user_object = document['user']
#     place_object = document['place']
#     user_id = user_object['id']
#
#     duplicate = 0
#
#     #check for duplicates
#     for x in range(len(filtered)):
#         if(filtered[x] == user_id):
#             duplicate = 1
#             print('dup found')
#             break
#
#     if(duplicate == 0):
#         profile_url = user_object['profile_image_url']
#         #ignore profiles with no profile image
#         if(profile_url != default_profile_url):
#             normal_image_url = profile_url
#             original_image_url = normal_image_url.replace("_normal","")
#             user_object['profile_image_url'] = original_image_url
#
#             data = {
#                 "image_url": original_image_url,
#                 "limit": detect_limit
#             }
#
#             #get face box with highest score
#             detect_response = requests.post(detect_api, data=data).json()
#             scores = detect_response['scores']
#             highest_score = 0
#             for x in range(1,detect_limit):
#                 if(scores[x] > scores[highest_score]):
#                     highest_score = x
#
#             face_pos = detect_response['faces'][highest_score]
#
#             new_user = {
#                 "user": user_object,
#                 "place": place_object,
#                 "face": face_pos,
#                 ""
#             }
#
#             #insert into filtereed DB
#             filtered_col.insert_one(new_user)
#             print("insert done")
