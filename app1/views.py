from django.shortcuts import render
from django.http import HttpResponse
import sys
from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2
import pyowm
from datetime import datetime
import csv
# import urllib3
import json
import time,requests
READ_API_KEY='PRI5OE83QRIQCSD8'
CHANNEL_ID= '1008189'
CHANNEL_ID1='1008513'
READ_API_KEY1='0UVE5H96EPPAF9JG'

def userdata(request):
    file_path="download.jpeg"
    project_id = "685884958596"
    model_id = "ICN5498450942321754112"
    with open(file_path,'rb') as ff:
        content=ff.read()
    data_Return=get_prediction(content,project_id,model_id)
    data_content=data_Return
    owm = pyowm.OWM('e433fbb81f694269bfdac51a5f90b438')  
    observation = owm.weather_at_coords(-0.107331,51.503614)
    w = observation.get_weather()
    m=w.get_temperature('celsius')
    temp_data=m
    data=[]
    with open("pestrec.csv") as csvfile:
        reader=csv.reader(csvfile)
        for row in reader:
            data.append(row)
    name=data_content.payload[0].display_name
    print(len(name))
    print(name)
    col=[x[0] for x in data]
    flag=0
    if name in col:
        for x in range(0,len(data)):
            if name==data[x][0]:
                print(data[x])
                flag=x
    else:
        print("Name don't")
    # TS=requests.get("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s"%(CHANNEL_ID,READ_API_KEY))
    #     # TS = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s"%(CHANNEL_ID,READ_API_KEY))

    # print (TS.json())
    # data=TS.json()
    # a = data['field1']
    # b = data['field2']
    # c = data['field3']
    # d = data['field4']
    # print (a)  
    # TS.close()  
    # while True:
    #     TS=requests.get("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s"%(CHANNEL_ID,READ_API_KEY))
    #     # TS = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s"%(CHANNEL_ID,READ_API_KEY))

    #     print (TS.json())
    #     data=TS.json()
    #     a = data['field1']
    #     b = data['field2']
    #     c = data['field3']
    #     d = data['field4']
    #     print (a)
    #     time.sleep(5)   

    #     TS.close()
    original={
        'data_content':data_content,
        'temp_data':temp_data,
        'data':data[flag],
        'name_of_pest':name,
        'pest_name':data[flag][1],
        'remedy':data[flag][3],
        'about':data[flag][2],
        'solution':"Use the {} for 3 months in affected area!".format(data[flag][3])
    }
    return render(request,'userdata.html',original)
def upload_image(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request,'upload.html')
def index(request):
    TS=requests.get("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s"%(CHANNEL_ID,READ_API_KEY))
    TS1=requests.get("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s"%(CHANNEL_ID1,READ_API_KEY1))
    print (TS.json())
    data=TS.json()
    a = data['field1']
    b = data['field2']
    c = data['field3']
    # d = data['field4']
    data1=TS1.json()
    d=data1['field1']
    print (a) 
    b=76.9717
    a=10.9281
    var=""
    print(type(d))
    c=int(c)
    if c==3:
        var="Heavy Rain,please take action"
    elif c==2:
        var="Moderate Rain, Your crops are feeling good!"
    elif c==1:
        var="No rain, Don't Worry"
    else:
        var="Hardware is Offline"
    weather=weather_data()
    temprature=get_weather_data()
    print(d)
    print(type(d))
    di=float(d)
    if di<30:
        sug="Moisture content is very poor"
    elif di<40:
        sug="Moisture content is depletion"
    elif di<50:
        sug="Moisture content is good enough"
    elif di<60:
        sug="Moisture content is saturated"
    else:
        sug="Moisture content might have exceeded due to water stagnation"
    content={
        'lon':a,
        'lat':b,
        'rain':c,
        'soil':d,
        'alert':var,
        'weather':weather,
        'temp':temprature,
        'sug':sug

    }
    TS.close()

    
    return render(request,'index.html',content)
def load_data(request):
    file_path="download.jpeg"
    project_id = "685884958596"
    model_id = "ICN5498450942321754112"
    with open(file_path,'rb') as ff:
        content=ff.read()
    data_Return=get_prediction(content,project_id,model_id)
    return HttpResponse("Image Data %s"%data_Return)

def get_prediction(content, project_id, model_id):
    prediction_client = automl_v1beta1.PredictionServiceClient()
    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'image': {'image_bytes': content }}
    params = {}
    request = prediction_client.predict(name, payload, params)
    return request

def weather_data(request):
    owm = pyowm.OWM('e433fbb81f694269bfdac51a5f90b438')  
    observation = owm.weather_at_coords(-0.107331,51.503614)
    w = observation.get_weather()
    m=w.get_temperature('celsius')
    return HttpResponse("Weather Data: %s"%m)   
def login(request):
    return render(request,'login.html')
def userdata_from_inde(request):
    TS=requests.get("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s"%(CHANNEL_ID,READ_API_KEY))
    print (TS.json())
    data=TS.json()
    a = data['field1']
    b = data['field2']
    c = data['field3']
    d = data['field4']
    print (a) 
    b=76.9717
    a=10.9281
    var=""
    print(type(d))
    # c=int(c)
    if c==3:
        var="Heavy Rain,please take action"
    elif c==2:
        var="Moderate Rain, Your crops are feeling good!"
    elif c==1:
        var="No rain, Don't Worry"
    else:
        var="Hardware is Offline"
    print(d)
    if d<30:
        sug="Moisture content is very poor"
    elif d<40:
        sug="Moisture content is depletion"
    elif d<50:
        sug="Moisture content is good enough"
    elif d<60:
        sug="Moisture content is saturated"
    else:
        sug="Moisture content might have exceeded due to water stagnation"
    weather=weather_data()
    temprature=get_weather_data()
    content={
        'lon':a,
        'lat':b,
        'rain':c,
        'soil':d,
        'alert':var,
        'weather':weather,
        'temp':temprature,
        'sug':sug

    }
    TS.close()

    
    return render(request,'hardware.html',content)
def weather_data():
    owm = pyowm.OWM('e433fbb81f694269bfdac51a5f90b438')  
    observation = owm.weather_at_coords(-0.107331,51.503614)
    w = observation.get_weather()
    m=w.get_temperature('celsius')
    return w
def get_weather_data():
    owm = pyowm.OWM('e433fbb81f694269bfdac51a5f90b438')  
    observation = owm.weather_at_coords(-0.107331,51.503614)
    w = observation.get_weather()
    m=w.get_temperature('celsius')
    return m
def test(request):
    TS=requests.get("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s"%(CHANNEL_ID,READ_API_KEY))
    print (TS.json())
    data=TS.json()
    a = data['field1']
    b = data['field2']
    c = data['field3']
    d = data['field4']
    print(a,b,c,d)
    content={
        'lan':a,
        'long':b,
        'soil':c,
        'rain':d
    }
    return render(request,'test.html',content)