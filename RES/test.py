import cv2
image = cv2.imread('lena.jpg')
t, in_img = cv2.imencode('.jpg', image)
input_jason = {'key':1, 'data':''}
import base64
input_jason['data'] = str(base64.b64encode(in_img), 'utf-8').replace('\n','').replace('\r','')
import json
data = json.dumps(input_jason)



