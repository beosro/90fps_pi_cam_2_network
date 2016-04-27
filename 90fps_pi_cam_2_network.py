#!/usr/bin/env python

#relies on gpac to convert the video
from socket import *
from picamera import *
from subprocess import *

recording_fps = 90
result_fps = 15

def getIP():
	 import subprocess
	 my_ip = subprocess.Popen(['ifconfig wlan0 | awk "/inet /" | cut -d":" -f 2 | cut -d" " -f1'], stdout=subprocess.PIPE, shell=True)
	 (IP,errors) = my_ip.communicate()
	 my_ip.stdout.close()
	 #if wlan0 gives error
	 if "error" in IP:
		my_ip = subprocess.Popen(['ifconfig eth0 | awk "/inet /" | cut -d":" -f 2 | cut -d" " -f1'], stdout=subprocess.PIPE, shell=True)
		(IP,errors) = my_ip.communicate()
		my_ip.stdout.close()
	 return IP

def makeVideo():
	#remove old videos
	Popen(["rm", "video.mp4", "video.h264"])
	with PiCamera() as camera:
	    camera.resolution = (640,480)
	    camera.framerate = recording_fps
	    camera.start_recording("video.h264")
	    camera.wait_recording(10) #length of video in seconds
	    camera.stop_recording()

	print("Video Recording at 90FPS finished")
	process = Popen(["MP4Box", "-fps", str(result_fps), "-add", "video.h264", "video.mp4"])
	process.wait()

def main():
	getIP()
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind((getIP(), 80))
	serverSocket.listen(1);

	while True:
		print 'Server ready'
		connectionSocket, addr = serverSocket.accept()
		makeVideo()
		f = open("video.mp4")
	    	outputdata = f.read()
	    	connectionSocket.send(outputdata)
	    	connectionSocket.close()

if __name__ == "__main__":
    main()
