image_types = [
    "normal",
    "glasses",
    "happy",
    "leftlight",
    "noglasses",
    "rightlight",
    "sad",
    "surprised",
    "sleepy",
    "wink"
]

num_people = 15

base_path = "faces_yale/"
original_path = "{}original/".format(base_path)
cropped_path = "{}cropped/".format(base_path)

base_url = 'http://115.146.92.137:8000/api/v1/'
detect_url = "{}face_detection".format(base_url)
compare_url = "{}face_comparison".format(base_url)

image_paths = []
cropped_image_paths = []

for y in range(num_people):

    temp1 = []
    temp2 = []

    for x in range(len(image_types)):

        if(y+1 < 10):
            person_id = "{}{}".format(0,y+1)
        else:
            person_id = "{}".format(y+1)

        temp_path1 = "{}{}_{}.png".format(original_path, person_id, image_types[x])
        temp1.append(temp_path1)
        temp_path2 = "{}{}_{}.png".format(cropped_path, person_id, image_types[x])
        temp2.append(temp_path2)

    image_paths.append(temp1)
    cropped_image_paths.append(temp2)
