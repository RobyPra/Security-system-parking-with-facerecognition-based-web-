from django.http.response import JsonResponse
from django.views import View
#from django.contrib.auth.views import LoginView, LogoutView
from .models import Person, Vehicle, Face
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, Http404
from .forms import FaceForm, FaceAuth
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
import random, string
from django.http import JsonResponse

class VerifView(View):
    template_name = 'verif/verification.html'

    def get(self, request):
        return render(request, self.template_name)


def faces_list(request):
    return render(request, 'verif/faces_list.html')

def faces_list_data(request):
    if request.method == 'GET':
        draw = int(request.GET.get('draw', 1))
        obj = Face.objects.all()
        queryset_and_total_count = faces_get_queryset_and_count(request)
        total_count = queryset_and_total_count.get('total_count')
        queryset = queryset_and_total_count.get('queryset')
        response_data = [{
            'id': Face.id,
            'ticketno': Face.ticketno,
            'name': Face.name,
            'dbface': Face.dbface,
        } for Face in queryset]
        return JsonResponse(
             {'draw': draw, 'recordsTotal': total_count, 'recordsFiltered': total_count, 'data': response_data})
    else:
        return JsonResponse({})

def faces_get_queryset_and_count(request):
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    total_count = Face.objects.all()
    queryset = Face.objects.all()
    total_count = total_count.count()

    order_column = request.GET.get('order[0][column]', None)
    if order_column == None:
        arguments='id'
    else:
        field = request.GET.get('columns['+order_column+'][data]', None)
        order = request.GET.get('order[0][dir]', None)
        if order == 'asc':
            arguments = field
        else:
            arguments = "-" + field


    search = request.GET.get('search[value]', None)
    if search:
        queryset = queryset.order_by(arguments).filter(Q(vihicle__icontains=search)|Q(name__icontains=search))[start:length + start]
    else:
        queryset = queryset.order_by(arguments)[start:length + start]
    return {'queryset': queryset, 'total_count': total_count}




def FaceCreate(request):
    if request.method == 'POST':
        form = FaceForm(request.POST, request.FILES)
        if form.is_valid():
            o = Face(ticketno = form.cleaned_data['ticketno'], name =form.cleaned_data['name'], 
                        faceid =form.cleaned_data['faceid'], )
            o.save()
            request.session['ticketno'] = form.cleaned_data['ticketno']
            return HttpResponseRedirect(reverse('model_train'))
        else:
            print('Form', form.errors)
    else:
        form = FaceForm()
    return render(request, 'verif/add_face.html', {'form': form})


def ModelTrain(request):
    return render(request, 'verif/dataset_and_training_of_model.html')

import cv2
import os
import numpy as np
from PIL import Image
import pickle

def CollectDataset(request):
    ticketnonumber = request.session['ticketno']
    faceobject = Face.objects.get(ticketno=ticketnonumber)
    foldername =str(faceobject.faceid)
    data_dir = 'database/images/'
   
    os.mkdir(os.path.join(data_dir, foldername))
    face_detector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height     
    print("\n [INFO] Initializing face capture. Look the camera and wait ...")   

        
    count = 0
    while (True):
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        print("\n [INFO]...", ret)
        print("\n [INFO]...", img)


        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            

            count += 1
            
            cv2.imwrite(os.path.join(data_dir, foldername + '/' + str(count) + '.jpg') , roi_gray)
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break
        elif count >= 30: # Take 30 face sample and stop video
             break

    print("\n [INFO] Exiting Program and cleanup stuff")
    cap.release()
    cv2.destroyAllWindows()

    return redirect('model_train')



def TrainingModel(request):
    
    image_dir = ('database/images/')
    face_detector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids ={}
    y_labels = []
    x_train = []

    for root , dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith('png') or file.endswith('jpg'):
                path = os.path.join(root, file)
                label = os.path.basename(root)
                print(label, path)
                if not label in label_ids:
                    label_ids[label] = current_id
                    current_id += 1
                id_ = label_ids[label]
                print(label_ids)
                pil_image = Image.open(path).convert('L')
                size = (640, 480)
                final_image = pil_image.resize(size, Image.ANTIALIAS)
                image_array = np.array(final_image, 'uint8')
                print(image_array)
                faces = face_detector.detectMultiScale(image_array,)

                for (x,y,w,h) in faces:
                    roi = image_array[y:y+h, x:x+w]
                    x_train.append(roi)
                    y_labels.append(id_)

    with open('pickles/face-labels.picle', 'wb') as f:
        pickle.dump(label_ids, f)

    recognizer.train(x_train, np.array(y_labels))
    recognizer.save('cascades/face-trainer.yml')






















    return redirect('model_train')

