from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.db.models import Avg
from .models import Register
from django.http.response import StreamingHttpResponse
from signup.camera import FaceDetect

from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import cv2,os
import numpy as np
#import matplotlib.pyplot as plt
import base64
import io
import face_recognition
from datetime import datetime,time,date,timedelta
from django.conf import settings
from .models import Profile , Profile_Out
from django.core.mail import EmailMessage
from django.template.loader import render_to_string






# Create your views here.

def home(request):
    return render(request,'home.html')

def logout(request):
    auth.logout(request)
    return render(request,'home.html')


def dashboard(request):
    if request.method=='POST':
        name=request.POST['name']
        dt=request.POST['dt']
        print(dt)


        if name:
            if Profile.objects.filter(name=name).exists():
                print("name")
                pro=Profile.objects.filter(name=name)
                # print(p)
                return render(request,'dashboard.html',{'pro':pro})
            else:
                messages.error(request, "No data found related to search")
                print("No data related to search")
                return render(request,'dashboard.html')
        else:
            if Profile.objects.filter(date=dt).exists():
                print("date")
                pro=Profile.objects.filter(date=dt)
                return render(request,'dashboard.html',{'pro':pro})
            else:
                messages.error(request, "No data related to search")
                print("No data found related to search")
                return render(request,'dashboard.html')
    else:
        print("dash")
        return render(request,'dashboard.html')


def signup(request):


    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        c_password=request.POST['c_password']

        if password==c_password:
            if User.objects.filter(username=name).exists():
                print("username taken!")
                messages.error(request,'Username taken!')
                return render(request,'signup.html')
            elif User.objects.filter(email=email).exists():
                print("email taken!")
                messages.error(request,'Already registred with same email!')
                return render(request,'signup.html')
            else:
                user=User.objects.create_user(username=name,password=password,email=email)
                user.save();
                messages.success(request,'Account Created Successfully!')
                print("user created")
                return render(request,'login.html')
        else:
            messages.error(request,'Password not matching!')
            print("password not matching!")
            return render(request,'signup.html')

    else:
        return render(request,'signup.html')


# global uname
def login(request):
    print("1")
    if request.method == 'POST':
        username=request.POST.get('name')
        password=request.POST.get('password')
        # print(email)
        print(password)
        user=auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            print("logedin!")

            return render(request,'home.html')
        else:
            print('invalid credentials!')
            messages.error(request,'Invalid credentials!')
            return render(request,'login.html')


    else:
        print("2")
        return render(request,'login.html')



def register(request):

    form=Register()
    if request.method=='POST':
        # form=Register(request.POST,request.FILES)
        # uname=request.POST['uname']
        fname=request.POST['fname']
        lname=request.POST['lname']
        add=request.POST['address']
        state=request.POST['state']
        zip=request.POST['zip']
        city=request.POST['city']
        email=request.POST['eaddress']
        pno=request.POST['phone']
        aadhar=request.POST['aadhar']
        professional=request.POST['typeofperson']
        salary=request.POST['salary']
        edate=request.POST['edate']
        pro_pic=request.FILES['pro_pic']
        print(pro_pic)
        import cv2
        img=cv2.imread(pro_pic)
        cv2.imshow("hello",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        print(professional)

        form.username=request.user
        print(form.username)
        form.first_name=fname
        form.last_name=lname
        form.add=add
        form.state=state
        form.zip_code=zip
        form.city=city
        form.email=email
        form.p_no=pno
        form.aadhar_no=aadhar
        form.profession=professional
        form.salary=salary
        form.join_date=edate
        form.pro_pic=pro_pic

        form.save()
        print("Data Saved!")
        messages.success(request,'Data Saved Successfully!')
        return render(request,'home.html')

    else:
        return render(request,'register.html')



# def gen(camera):


#     while True:
        
#         frame = camera.get_frame()
#         # if face.x:
#         #     break
#         yield (b'--frame\r\n'
# 				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# def facecam_feed(request):
# 	return StreamingHttpResponse(gen(FaceDetect()),
# 					content_type='multipart/x-mixed-replace; boundary=frame')



def profile(request):

    
    log_user=request.user
    print(f'log_user:{log_user}')
    # log=log_user.upper()
    register=Register.objects.get(username=log_user)
    pro=Profile.objects.filter(name=log_user)
    # print(pro.profession)
    # x=[x.date for x in pro]
    # y=[y.attendance for y in pro]
    # chart=FaceDetect.get_plot(x,y)
    # print(pro.name)
    # name=register.first_name
    # print(name)
    # print(register.first_name)    
    return render(request,'profile.html',{"register":register,"pro":pro})


def graph(request):
    log_user=request.user
    pro=Profile.objects.filter(name=log_user)
    x=[x.date for x in pro]
    y=[y.attendance for y in pro]
    # x=[1,2,1,3,4,5,6,7,8,9,10]
    # y=[1,2,1,3,4,5,6,7,8,9,10]
    chart=FaceDetect.get_plot(x,y)
    return render(request,'graph.html', {"chart":chart})




def train(request):
    path = './dataset'
    images=[]
    global classNames
    classNames=[]
    mylist=os.listdir(path)
    print(mylist)

    for cls in mylist:
        curImg=cv2.imread(f'{path}/{cls}')
    #     print(f'{path}/{cls}')
        images.append(curImg)
        classNames.append(os.path.splitext(cls)[0])
        
    print(classNames)

    # encodeListKnown=findEncodings(images)
    encodeList=[]
    i=0
    for img in images:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        i+=1
        print(i)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    global encodeListKnown
    encodeListKnown=encodeList
    print("Encoding complete!")
    messages.success(request,'Dataset trained Successfully!')
    return render(request, 'home.html')


def facecam_feed(request):

    log_user=request.user
    register=Register.objects.get(username=log_user)
    # messages.info(request, "Please Wait! Cammera will open in a while")
    vs = VideoStream(src=0).start()
		# start the FPS throughput estimator
    fps = FPS().start()


    while True:
        frame = vs.read()
        frame = cv2.flip(frame,1)

        # resize the frame to have a width of 600 pixels (while
        # maintaining the aspect ratio), and then grab the image
        # dimensions
        # frame = imutils.resize(frame, width=600)
        # (h, w) = frame.shape[:2]


        # res,img=cap.read()
        # imgSmall=cv2.resize(frame,(0,0),None,0.25,0.25)
        imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        facesCurFrame= face_recognition.face_locations(imgRGB)
        encodeCurFrame=face_recognition.face_encodings(imgRGB,facesCurFrame)
        
        for encodeFace,FaceLoc in zip(encodeCurFrame,facesCurFrame):
            matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
            print(faceDis)
            name='UNKNOWN'
            matchIndex=np.argmin(faceDis)
        
            if matches[matchIndex]:
                print(f'index:{matchIndex}')
                name=classNames[matchIndex]
                print(name)
            y1,x2,y2,x1=FaceLoc
            # y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),1)
            cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

        cv2.imshow("Press 'q' to exit cammera!",frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

            # matchIndex=np.argmin(faceDis)
            
            # if matches[matchIndex]:
            #     # now=datetime.now()
            #     # print(now)
            #     name=classNames[matchIndex]
            #     print(name)
            #     y1,x2,y2,x1=FaceLoc
            #     # y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            #     cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),1)
            #     cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            #     cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

    # vs.stop()
    # cv2.destroyAllWindows()



    now=datetime.now()
    t1=now.time()
    pro=Profile()
    # pro.name=name
    # if name=='UNKNOWN':
    #     return render(request, "register.html")
    pro.date=now.date()
    pro.time=now.time()
    # cv2.imshow("Press 'q' to exit cammera!",frame)
    if name=='UNKNOWN':
        vs.stop()
        cv2.destroyAllWindows()
        return render(request, "register.html")
    elif name in ['Modiji']:
        email=EmailMessage(
        'Alert!!',
        'Suspicious {{name}} enterd into office',
        settings.EMAIL_HOST_USER,
        [register.email],
        print(register.email)
        )
        email.send()
        pro.name=name
    else:
        pro.name=name
            # messages.info(request, "Press 'q' to exit cammera")

        # if cv2.waitKey(1) & 0xFF==ord('q'):
        #     break
            # messages.info(request, "Your attendance is taken! Cammera will shutdown in a while")
        fps.update()
    # ret, jpeg = cv2.imencode('.jpg', frame)
    # return jpeg.tobytes()


    # t2=Profile.objects.filter(name=pro.name).aggregate(Avg('time'))
    # print(t2)


    # t2=Profile.objects.annotate(Avg('time') ,filter=Q(name=pro.name))
    t2=Profile.objects.filter(name=pro).aggregate(time_avg=Avg('time'))
    print(t2)
    # t2=time(t2)

    # tot=Profile.objects.filter(name=pro.name).count()
    # t_tot=Profile.objects.filter(name=pro).aggregate(Avg('time'))
    # print(tot)
    # print(t_tot)
    # t2=(t2/tot)*100


    # for i in range(tot):
                
    t2=(datetime.min+t2['time_avg']).time()
    print(t2)
    print(type(t2))

    # datetime.combine(date.today(), t2) - datetime.combine(date.today(), t1)

    t=time(00,30,00)
    # dat=date(1, 1,1)
    # datetime1=datetime.combine(dat,t)
    # datetime2=datetime.combine(dat,t2)

    t2_before=datetime.combine(date.today(), t2) - datetime.combine(date.today(), t)
    print(t2_before)
    print(type(t2_before))
    t2_after=datetime.combine(date.today(), t2) +timedelta(hours=0.5)
    print(t2_after)
    print(type(t2_after))

    t2_before=(datetime.min+t2_before).time()
    # t2_before=(datetime.min+t2_before).time()

    # t2=time(10,00,00)
    if t1<t2_before or t1>t2_after.time():
    # if t1>t2:
        # pro=Profile()
        pro.attendance=False
        messages.success(request,'Abnormal time detected!')
        # email=EmailMessage(
        # 	'Less Attendance',
        # 	'You are late , your attendance is marked as absent',
        # 	settings.EMAIL_HOST_USER,
        # 	[register.email],
        # 	print(register.email)
        # )
        # email.send()
        pro.abnormal=True
        # pro.save()
        print("abnormal time !")
    else:
        pro.attendance=True
        pro.abnornal=False
        print("On time!")
    pro.save()
    # log_user=request.user
    tot=Profile.objects.filter(name=pro.name).count()
    t_tot=Profile.objects.filter(name=pro.name,attendance=True).count()
    print(tot)
    print(t_tot)
    avg=(t_tot/tot)*100
    if avg <80:

        template=render_to_string('email.html',{'name':pro.name,'avg':avg})

        email=EmailMessage(
        	'Reg: Attendance',
        	template,
        	settings.EMAIL_HOST_USER,
        	[register.email],
        	print(register.email)
        )
        email.send()

        print("Your Attendance is less than 80%")
    else:
        print("attendance is more than 80%")
    vs.stop()
    cv2.destroyAllWindows()
    # if name=='UNKNOWN':
    #     return render(request,'register.html')
    # messages.success(request,'Data Saved Successfully!')
    return render(request,'home.html')







def facecam_feed_out(request):

    log_user=request.user
    register=Register.objects.get(username=log_user)
    # messages.info(request, "Please Wait! Cammera will open in a while")
    vs = VideoStream(src="rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov").start()
		# start the FPS throughput estimator
    fps = FPS().start()

    
    while True:
        frame = vs.read()
        frame = cv2.flip(frame,1)

        # resize the frame to have a width of 600 pixels (while
        # maintaining the aspect ratio), and then grab the image
        # dimensions
        # frame = imutils.resize(frame, width=600)
        # (h, w) = frame.shape[:2]


        # res,img=cap.read()
        # imgSmall=cv2.resize(frame,(0,0),None,0.25,0.25)
        imgRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
        facesCurFrame= face_recognition.face_locations(imgRGB)
        encodeCurFrame=face_recognition.face_encodings(imgRGB,facesCurFrame)
        
        for encodeFace,FaceLoc in zip(encodeCurFrame,facesCurFrame):
            matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
            print(faceDis)
            name='UNKNOWN'
            matchIndex=np.argmin(faceDis)
        
            if matches[matchIndex]:
                print(f'index:{matchIndex}')
                name=classNames[matchIndex]
                print(name)
            y1,x2,y2,x1=FaceLoc
            # y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),1)
            cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

        cv2.imshow("Press 'q' to exit cammera!",frame)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

            # matchIndex=np.argmin(faceDis)
            
            # if matches[matchIndex]:
            #     # now=datetime.now()
            #     # print(now)
            #     name=classNames[matchIndex]
            #     print(name)
            #     y1,x2,y2,x1=FaceLoc
            #     # y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            #     cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),1)
            #     cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            #     cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)

    # vs.stop()
    # cv2.destroyAllWindows()



    now=datetime.now()
    t1=now.time()
    pro=Profile_Out()
    # pro.name=name
    # if name=='UNKNOWN':
    #     return render(request, "register.html")
    pro.date=now.date()
    pro.time=now.time()
    # cv2.imshow("Press 'q' to exit cammera!",frame)
    # if name=='UNKNOWN':
    #     vs.stop()
    #     cv2.destroyAllWindows()
    #     return render(request, "register.html")
    if name in ['Modiji']:
        email=EmailMessage(
        'Alert!!',
        'Suspicious  enterd into office',
        settings.EMAIL_HOST_USER,
        [register.email],
        print(register.email)
        )
        email.send()
        pro.name=name
    else:
        pro.name=name
            # messages.info(request, "Press 'q' to exit cammera")

        # if cv2.waitKey(1) & 0xFF==ord('q'):
        #     break
            # messages.info(request, "Your attendance is taken! Cammera will shutdown in a while")
        fps.update()
    # ret, jpeg = cv2.imencode('.jpg', frame)
    # return jpeg.tobytes()


    # t2=Profile.objects.filter(name=pro.name).aggregate(Avg('time'))
    # print(t2)


    # t2=Profile.objects.annotate(Avg('time') ,filter=Q(name=pro.name))
    t2=Profile.objects.filter(name=pro).aggregate(time_avg=Avg('time'))
    print(t2)
    # t2=time(t2)

    # tot=Profile.objects.filter(name=pro.name).count()
    # t_tot=Profile.objects.filter(name=pro).aggregate(Avg('time'))
    # print(tot)
    # print(t_tot)
    # t2=(t2/tot)*100


    # for i in range(tot):
                
    t2=(datetime.min+t2['time_avg']).time()
    print(t2)
    print(type(t2))

    # datetime.combine(date.today(), t2) - datetime.combine(date.today(), t1)

    t=time(00,30,00)
    # dat=date(1, 1,1)
    # datetime1=datetime.combine(dat,t)
    # datetime2=datetime.combine(dat,t2)

    t2_before=datetime.combine(date.today(), t2) - datetime.combine(date.today(), t)
    print(t2_before)
    print(type(t2_before))
    t2_after=datetime.combine(date.today(), t2) +timedelta(hours=0.5)
    print(t2_after)
    print(type(t2_after))

    t2_before=(datetime.min+t2_before).time()
    # t2_before=(datetime.min+t2_before).time()

    # t2=time(10,00,00)
    if t1<t2_before or t1>t2_after.time():
    # if t1>t2:
        # pro=Profile()
        pro.attendance=False
        messages.success(request,'Abnormal time detected!')
        # email=EmailMessage(
        # 	'Less Attendance',
        # 	'You are late , your attendance is marked as absent',
        # 	settings.EMAIL_HOST_USER,
        # 	[register.email],
        # 	print(register.email)
        # )
        # email.send()
        pro.abnormal=True
        # pro.save()
        print("abnormal time !")
    else:
        pro.attendance=True
        pro.abnornal=False
        print("On time!")
    pro.save()
    # log_user=request.user
    # tot=Profile.objects.filter(name=pro.name).count()
    # t_tot=Profile.objects.filter(name=pro.name,attendance=True).count()
    # print(tot)
    # print(t_tot)
    # avg=(t_tot/tot)*100
    # if avg <80:

    #     template=render_to_string('email.html',{'name':pro.name,'avg':avg})

    #     email=EmailMessage(
    #     	'Reg: Attendance',
    #     	template,
    #     	settings.EMAIL_HOST_USER,
    #     	[register.email],
    #     	print(register.email)
    #     )
    #     email.send()

    #     print("Your Attendance is less than 80%")
    # else:
    #     print("attendance is more than 80%")
    vs.stop()
    cv2.destroyAllWindows()
    # if name=='UNKNOWN':
    #     return render(request,'register.html')
    # messages.success(request,'Data Saved Successfully!')
    return render(request,'home.html')