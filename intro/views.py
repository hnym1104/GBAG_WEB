from django.shortcuts import render
from tensorflow.keras.models import load_model
from .load_PLModel import *
from .visualize_test import *

# Create your views here.
def home(request):
  return render(request,'index.html')

def introduction(request):
  return render(request,'introduction.html')

def result(request):
  azi=request.POST['azi']
  down=request.POST['down']
  pci=request.POST['pci']

  ''' pci,azi,down loadPLModel load_input 함수 호출해서 보내면 될듯'''
  img_input, numeric_input = load_input(pci,azi,down) #인풋데이터 불러옴
  PLModel = load_model("C:\\GBAG_WEB\\gbag\\static\\PLModel\\gbag_0520_760.h5")
  predictions = PLModel.predict([img_input, numeric_input]) #예측함
  visualize_result(pci,azi,down,predictions) #시각화 함수 호출, 이미지 생성해줌
  return render(request,'result.html',{'azi':azi,'down':down,'pci':pci})


def predict(request):
  return render(request,'predict.html')


