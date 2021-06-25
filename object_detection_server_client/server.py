import socket
import requests
import cv2 as cv
import numpy as np
import os

whT = 320
confThreshold = 0.5
nmsThreshold = 0.2
execution_path = os.getcwd()

#### LOAD MODEL
## Coco Names
classesFile = os.path.join(execution_path , "coco.names")
classNames = []
with open(classesFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")
## Model Files
modelConfiguration = os.path.join(execution_path , "yolov3-320.cfg")
modelWeights = os.path.join(execution_path , "yolov3.weights")
net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

def findObjects(outputs,img):
    objects = list()
    hT, wT, cT = img.shape
    bbox = []
    classIds = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                w,h = int(det[2]*wT) , int(det[3]*hT)
                x,y = int((det[0]*wT)-w/2) , int((det[1]*hT)-h/2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv.dnn.NMSBoxes(bbox, confs, confThreshold, nmsThreshold)

    for i in indices:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        # print(x,y,w,h)
        cv.rectangle(img, (x, y), (x+w,y+h), (255, 0 , 255), 2)
        cv.putText(img,f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%',(x, y-10), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
        objects.append(classNames[classIds[i]])

    return objects

HOST = '127.0.0.1'
PORT = 24680

def openConnection():

	client_socket = None
	client_addr = None

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind((HOST, PORT))
	sock.listen(1)
	while True:
		client_socket, client_addr = sock.accept()
		if client_addr != None: break

	return client_socket, client_addr

def startCommunication(client_conn, client_addr):
	client_conn.sendall(bytes("Hi there, Welcome to the image recognition server!", 'utf-8'))
	client_conn.sendall(bytes(">>> Please enter the image url below : \n", 'utf-8'))

	image_url = client_conn.recv(1024).decode('utf-8')

	local_file = open('local_file.jpg','wb')
	resp = requests.get(image_url, stream=True)

	local_file.write(resp.content)
	local_file.close()

	img = cv.imread(os.path.join(os.getcwd() , "local_file.jpg"))
	blob = cv.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
	net.setInput(blob)
	layersNames = net.getLayerNames()
	outputNames = [(layersNames[i[0]-1]) for i in net.getUnconnectedOutLayers()]
	outputs = net.forward(outputNames)
	objects = findObjects(outputs,img)

	print(objects)

	obj = dict()
	for i in objects:
		if(i not in obj.keys()):
			obj[i] = 0

	for i in obj.keys():
		for j in objects:
			if i == j:
				obj[i] = obj[i] + 1

	flag = 1
	while True:
		cv.imshow("Image", img)
		if flag == 1:
			client_conn.sendall(bytes("\n" + str(obj), 'utf-8'))
			flag = flag + 1
		cv.waitKey(1)



client_conn, client_addr = openConnection()
startCommunication(client_conn, client_addr)
client_conn.close()
