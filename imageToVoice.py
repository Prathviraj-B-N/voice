import cv2              # capturing/processing image     
from time import sleep  # stop execution for few seconds              
import boto3            # Library required to use aws
import os               # System path related operations
from gtts import gTTS   # Library required to convert text to voice

X = 'AKIA553AZGA3XY2KDXM2'                          # AWS api key , no longer valid . store this in .env for security
Y = 'l3MpZeZ6pdrSpx2pvkfTMage0wkEaoVpsC2gqoWl'

key = cv2. waitKey(1)                               # starts expecting a keypress
webcam = cv2.VideoCapture(0)                        # starts webcam

os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'
access_key_id = X
secret_access_key = Y

sleep(2)                                            # warmup time for camera

while True:

    try:
        check, frame = webcam.read()                # returns image frame by frame each second     
        
        # print(check) #prints true as long as the webcam is running
        # print(frame) #prints matrix values of each framecd
        
        cv2.imshow("Capturing", frame)              # shows video on screen
        key = cv2.waitKey(1)                        # starts expecting a keypress
        if key == ord('s'):                         # When key 's' is pressed current frame[image] is saved as saved_img.jpg
            cv2.imwrite(filename='saved_img.jpg', img=frame)
            webcam.release()
            print("Processing image...")
            
            #img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR) # loads image into img_ variable
            #print("Converting RGB image to grayscale...")
            #gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
            #print("Converted RGB image to grayscale...")
            #img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=gray)
            #print("Image saved!")

            break
    # to quit in middle
        elif key == ord('q'):   
            webcam.release()         # releases webcam
            cv2.destroyAllWindows()  # closes open windows if any
            break

    except(KeyboardInterrupt):       # handle errors 
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
    
    
# pass captured image to AWS


photo = 'saved_img.jpg'

client = boto3.client('rekognition',
                      aws_access_key_id = access_key_id,
                      aws_secret_access_key = secret_access_key)           #create an aws client to access API rekognition

with open(photo , 'rb') as source_image:
    source_bytes = source_image.read()         #convert rgb image to byte code

response = client.detect_text(Image={'Bytes':source_bytes}
                              )                              #will return json 

#print(response)
#GTTS
arr = []
print('[converting]')

for item in response['TextDetections']:           # response['TextDetections'] = {{"Type":"LINE","DetectedText":"Example text"},{}}
        if (item['Type']== 'LINE'):
            arr.append(item['DetectedText'])
   
language = 'en'
modifiedName = ' '.join(arr)
myobj = gTTS(text=modifiedName, lang=language, slow=False)
myobj.save("name.mp3")
os.system("mpg321 name.mp3")
            
#for item in response['TextDetections']:
#            print(item['DetectedText'] + " ")
            
cv2.destroyAllWindows()
