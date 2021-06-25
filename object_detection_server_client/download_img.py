import requests
local_file = open('local_file.png','wb')
image_url = "https://www.dev2qa.com/demo/images/green_button.jpg"
resp = requests.get(image_url, stream=True)
local_file.write(resp.content)
local_file.close()
