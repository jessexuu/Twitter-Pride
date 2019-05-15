from PIL import Image
import requests
import json
import variables

#use cropped image or original
use_cropped = 1

for y in range (len(variables.image_paths)):

    sim_confidence = []

    for x in range (1, len(variables.image_types)):

        if(use_cropped):
            default_image = open(variables.cropped_image_paths[0][0], "rb")
        else:
            default_image = open(variables.image_paths[0][0], "rb")

        files = {
            "face_1": default_image,
            "face_2": open(variables.cropped_image_paths[0][x], "rb")
        }

        compare_response = requests.post(compare_url, files=files).json()
        similarity = compare_response['similarity']
        sim_confidence.append(similarity)

    print(sim_confidence)
    sum =0

    for x in range(len(sim_confidence)):
        sum += sim_confidence[x]

    average = sum/len(sim_confidence)
    print(average)
