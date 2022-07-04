import boto3
import csv
from PIL import Image, ImageDraw, ImageFont
import io

with open('credentials.csv', 'r') as file:
    next(file)
    reader = csv.reader(file)

    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]


client = boto3.client('rekognition', region_name='us-west-2',
                        aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

photo = 'people.jpeg'

with open(photo, 'rb') as image_file:
    source_bytes = image_file.read()


detect_objects = client.detect_labels(Image={'Bytes': source_bytes})
# print(detect_objects)

image = Image.open(io.BytesIO(source_bytes))
draw = ImageDraw.Draw(image)

for label in detect_objects['Labels']:
    print(label["Name"])
    print("Confidence: ", label["Confidence"])

    for instances in label['Instances']:
        if 'BoundingBox' in instances:

            box = instances["BoundingBox"]

            left = image.width * box['Left']
            top = image.height * box['Top']
            width = image.width * box['Width']
            height = image.height * box['Height']

            points = (
                        (left,top),
                        (left + width, top),
                        (left + width, top + height),
                        (left , top + height),
                        (left, top)
                    )
            draw.line(points, width=5, fill = "#69f5d9")

            shape = [(left - 2, top - 35), (width + 2 + left, top)]
            draw.rectangle(shape, fill = "#69f5d9")

            font = ImageFont.truetype("arial.ttf", 30)

            draw.text((left + 170, top - 30), label["Name"], font=font, fill='#000000')


image.show()
