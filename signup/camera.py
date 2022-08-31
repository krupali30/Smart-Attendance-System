from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import cv2,os
import numpy as np
import matplotlib.pyplot as plt
import base64
import io
# import graph_nets as gn
# import sonnet as snt
import face_recognition
from datetime import datetime,time
from django.conf import settings
from .models import Profile
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string



class FaceDetect(object):
	 
	def __init__(self):

		pass
		# self.vs = VideoStream(src=0).start()
		# # start the FPS throughput estimator
		# self.fps = FPS().start()

		# path = './dataset'
		# images=[]
		# self.classNames=[]
		# mylist=os.listdir(path)
		# print(mylist)

		# for cls in mylist:
		# 	curImg=cv2.imread(f'{path}/{cls}')
		# #     print(f'{path}/{cls}')
		# 	images.append(curImg)
		# 	self.classNames.append(os.path.splitext(cls)[0])
			
		# print(self.classNames)

		# # encodeListKnown=findEncodings(images)
		# encodeList=[]
		# i=0
		# for img in images:
		# 	img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		# 	i+=1
		# 	print(i)
		# 	encode=face_recognition.face_encodings(img)[0]
		# 	encodeList.append(encode)

		# self.encodeListKnown=encodeList
		# print("Encoding complete!")



	def __del__(self):
		pass
		# t2=time(18,0,0,0)
		
		# if self.t1 > t2:
		# 	# pro=Profile()
		# 	self.pro.attendance=False
		# 	# pro.save()
		# 	print("abnormal time !")
		# else:
		# 	self.pro.attendance=True
		# # self.pro.username=
		# self.pro.save()
		# # log_user=request.user
		# tot=Profile.objects.filter(name=self.pro.name).count()
		# t_tot=Profile.objects.filter(name=self.pro.name,attendance=True).count()
		# print(tot)
		# print(t_tot)
		# avg=(t_tot/tot)*100
		# if avg <80:

			# template=render_to_string('email.html')

			# email=EmailMessage(
			# 	'Less Attendance',
			# 	template,
			# 	settings.EMAIL_HOST_USER,
			# 	[],
			# 	# print(self.pro.username.email)
			# )
			# email.send()

		# 	print("Your Attendance is less than 80%")
		# else:
		# 	print("attendance is more than 80%")
		# self.vs.stop()
		# cv2.destroyAllWindows()


	# def get_frame(self):

	# 	frame = self.vs.read()
	# 	frame = cv2.flip(frame,1)

	# 	# resize the frame to have a width of 600 pixels (while
	# 	# maintaining the aspect ratio), and then grab the image
	# 	# dimensions
	# 	# frame = imutils.resize(frame, width=600)
	# 	# (h, w) = frame.shape[:2]


	# 	# res,img=cap.read()
	# 	# imgSmall=cv2.resize(frame,(0,0),None,0.25,0.25)
	# 	imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		
	# 	facesCurFrame= face_recognition.face_locations(imgRGB)
	# 	encodeCurFrame=face_recognition.face_encodings(imgRGB,facesCurFrame)
		
	# 	for encodeFace,FaceLoc in zip(encodeCurFrame,facesCurFrame):
	# 		matches=face_recognition.compare_faces(self.encodeListKnown,encodeFace)
	# 		faceDis=face_recognition.face_distance(self.encodeListKnown,encodeFace)
	# 		print(faceDis)
	# 		matchIndex=np.argmin(faceDis)
			
	# 		if matches[matchIndex]:
	# 			# now=datetime.now()
	# 			# print(now)
	# 			name=self.classNames[matchIndex]
	# 			print(name)
	# 			y1,x2,y2,x1=FaceLoc
	# 			# y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
	# 			cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),1)
	# 			cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
	# 			cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
				
	# 			now=datetime.now()
	# 			self.t1=now.time()
	# 			self.pro=Profile()
	# 			self.pro.name=name
	# 			self.pro.date=now.date()
	# 			self.pro.time=now.time()

	# 	self.fps.update()
	# 	ret, jpeg = cv2.imencode('.jpg', frame)
	# 	return jpeg.tobytes()



	def get_plot(x,y):
		plt.switch_backend('AGG')
		plt.figure(figsize=(10,5))
		plt.title('Attendance Report')
		plt.bar(x,y)
		# plt.xticks(rotation=100)
		plt.xlabel("Date")
		plt.ylabel("Attendance")
		# plt.show()
		plt.tight_layout()
		flike = io.BytesIO()
		plt.savefig(flike)
		b64 = base64.b64encode(flike.getvalue()).decode()
		# buffer.close()
		return b64