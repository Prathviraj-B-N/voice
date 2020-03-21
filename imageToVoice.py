# click picture
import cv2
from time import sleep
import csv
import boto3
import os
from gtts import gTTS

X = 'AKIA553AZGA3XY2KDXM2'
Y = 'l3MpZeZ6pdrSpx2pvkfTMage0wkEaoVpsC2gqoWl'

key = cv2. waitKey(1)
webcam = cv2.VideoCapture('rtsp://192.168.43.117:8080/h264_ulaw.sdp')

os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'
access_key_id = X
secret_access_key = Y

sleep(2)

while True:

    try:
        check, frame = webcam.read()
        print(check) #prints true as long as the webcam is running
        print(frame) #prints matrix values of each framecd
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(filename='saved_img.jpg', img=frame)
            webcam.release()
            print("Processing image...")
            img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
            #print("Converting RGB image to grayscale...")
            #gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
            #print("Converted RGB image to grayscale...")
            #img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=gray)
            #print("Image saved!")

            break

        elif key == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break

    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
    
    
# pass to AWS


photo = 'saved_img.jpg'

client = boto3.client('rekognition',
                      aws_access_key_id = access_key_id,
                      aws_secret_access_key = secret_access_key)

with open(photo , 'rb') as source_image:
    source_bytes = source_image.read()

response = client.detect_text(Image={'Bytes':source_bytes}
                              )

#print(response)
#GTTS
arr = []
print('[converting]')
language = 'en'
for item in response['TextDetections']:
        if (item['Type']== 'LINE'):
            arr.append(item['DetectedText'])
   

modifiedName = ' '.join(arr)
myobj = gTTS(text=modifiedName, lang=language, slow=False)
myobj.save("name.mp3")
os.system("mpg321 name.mp3")
            
for item in response['TextDetections']:
            print(item['DetectedText'] + " ")
            
cv2.destroyAllWindows()
