import requests
import json
from PIL import Image
import variables

for y in range(variables.num_people):

    for x in range(len(variables.image_paths[y])):

        files = {
            "image_file" : open(variables.image_paths[y][x], 'rb')
        }

        data = {
            "limit" : 3
        }

        detect_response = requests.post(variables.detect_url, files=files, data=data).json()
        scores = detect_response['scores']

        highest_score = 0

        for z in range(1,3):
            if(scores[z] > scores[highest_score]):
                highest_score = z

        face_position = detect_response['faces'][highest_score]

        temp = Image.open(variables.image_paths[y][x])
        width, height = temp.size

        top = face_position[0] * height
        left = face_position[1] * width
        right = face_position[3] * width
        bottom = face_position[2] * height

        cropped = temp.crop((int(left), int(top), int(right), int(bottom)))
        cropped.save(variables.cropped_image_paths[y][x])
        print("face {} {} done".format(y+1,variables.image_types[x]))
