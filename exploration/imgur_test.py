import urllib
import base64
import os
import re
import json

url = 'http://api.imgur.com/2/upload.json'
apikey = '475add36e0e43bd3d3c4510fd436e8e2'
image_name = 'F:\\Documents\\AssaultCube_v1.1\\screenshots\\20120603_16.15.07_ac_desert_TOSOK.jpg'

def encode_image(path_to_image):
    source = open(path_to_image, 'rb')
    picture = base64.b64encode(source.read())
    print('encoded')
    return picture

def upload_image(path_to_image):
    picture = encode_image(path_to_image)
    parameters = { 'key' : apikey, 'image' : picture }

    data = urllib.urlencode(parameters)
    print('sending')
    json_handle = urllib.urlopen(url, data)

    print('received response from server')
    print json.loads(json_handle.read())

path_to_image = os.path.join(os.getcwd(), image_name)
upload_image(path_to_image)
