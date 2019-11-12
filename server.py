#-*- coding:utf-8 -*-

import os,sys

from flask import Flask, redirect, url_for, request,send_file

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types



from konlpy.tag import Okt
okt = Okt()
import numpy
from functools import reduce

from konlpy.tag import Komoran
#komoran = Komoran(userdic='/tmp/dic.txt')
from konlpy.tag import Kkma
kkma = Kkma()

test=[u'초기화를 위한 테스트 문구입니다.']

# global #
names = []
menus = []
unknown=''

########################################################

app = Flask(__name__)

@app.route('/synth',methods=['POST'])
def synth_call():
    print('synth call')
    text = request.form['text']

if __name__ == '__main__':
   #app.run(debug = True)
   # 모든 ip (외부 ip) 에서 접근 가능하도록 설정.
   app.run(host='0.0.0.0',port = 1170)


#############################################   

# [START speech_transcribe_sync]

def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    client = speech.SpeechClient()
    now = datetime.datetime.now()
    speech_file= os.getcwd() + '/'+  speech_file
    # [START speech_python_migration_sync_request]
    # [START speech_python_migration_config]
    outstr = ''
    try:
        #print(os.path.isfile(speech_file) )
        if(debug):
            print('Python::opening file ' + speech_file)
        with io.open(speech_file, 'rb') as audio_file:
            content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code='ko-KR')
        # [END speech_python_migration_config]

        # [START speech_python_migration_sync_response]
        if(debug):
            print('GCP::requesting : '  +speech_file )
        response = client.recognize(config, audio)
        # [END speech_python_migration_sync_request]
        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        # The first alternative is the most likely one for this portion.
        #output_transcription = response.results[0].alternatives[0].transcript
        if(debug):
            print('opening response file') 
        outfile = open('response.txt','a')
        for result in response.results:

            if(os.name == 'posix'):
                outstr =(result.alternatives[0].transcript)
            else :
                #                outstr =(result.alternatives[0].transcript).encode("utf-8")
                outstr =(result.alternatives[0].transcript)

#            outstr = result.alternatives[0].transcript
            if(debug):
                print('GCP::response : ' + outstr)
            #outstr = result.alternatives[0].transcript
            #print(u'Transcript: {}'.format(result.alternatives[0].transcript))
            #print(outstr.format(result.alternatives[0].transcript))
            outfile.write(now.strftime("%Y-%m-%d %H:%M") + " : " + outstr)
            outfile.write('\n')
            #outfile.write(outstr)
        print("GCP-response::"+outstr)    
        #outfile.write(output_transcription)
        #outfile.write(response.results[0].alternatives[0].transcript)
        outfile.close()
#        print('closing response file')
    except:
        #outfile = open('output.txt', 'w')
        outfile = open('response.txt','a')
        outfile.write(now.strftime("%Y-%m-%d %H:%M") + " : " + "ERROR\n")
        #outfile.write('recognition error occured')
        outfile.close()
        outstr = 'ERROR::exeption occured in GCP-Speech'
        print(outstr)
        #outfile.write("error")
        #outfile.close()
        # [END speech_python_migration_sync_response]
    # [END speech_transcribe_sync]
#    print('got ' + outstr)

    if(outstr ==""):
        return "<내용 없음>"
    return outstr
#return outstr
        #return str(outstr, "utf-8")

def init():
    global menus
    global names
    key_path = os.getcwd() + "KEY/key.json"
    key_path = os.path.normpath(key_path)
#    input_path = os.getcwd() + "/output.wav"
    #input_path = os.getcwd() + file_name

    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     'speech_folder', help='Full path of audio file folder to be recognized')
    # args = parser.parse_args()
    # transcribe_file(args.speech_folder)
#    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/bonhyeok/git/IIP_DEMO/KEY/key.json"
#    transcribe_file('/home/bonhyeok/git/IIP_DEMO/build/output.wav')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=key_path
    #print(input_path)
    kkma.pos(test[0])

    with open("/config/inst.json") as json_file:
        json_data = json.load(json_file)
        names = json_data["name"]
        menus = json_data["menu"]


    print('NOTE::Python Module initialized')


### Chatbot Engine 


def analyze_intent(line):
    global unknown
    pos = kkma.pos(line)
    #print(pos)
    noun = kkma.nouns(line)
    call = False
    number = []
    #posdict = dict(pos)
    for intent in callintent:
        call = call or intent in pos
    menu = False
    for intent in menuintent:
        menu = menu or intent in pos
    if call:
        name_included_boolean = numpy.array(list(map(lambda x : line.startswith(x), names)))#find names from start
        if(len(noun)!=0):
            a = max(noun, key=len)
            name_included_boolean = name_included_boolean | numpy.array(list(map(lambda x : x in a, names))) #check names included in noun

        name_included_index = (numpy.where(name_included_boolean)[0])
        if len(name_included_index) == 0:
            return 100
        else:
            return int(100+name_included_index[0])

    elif menu:
        menu_included_boolean = list(map(lambda x : sum([x in n for n in noun])!=0 , menus))
        #print(menu_included_boolean)
        menu_included_index = (numpy.where(menu_included_boolean)[0])
        if len(menu_included_index) == 0:
            return 200
        else:
            return int(200+menu_included_index[0])
    else:
        print("???? ::" + str(line))
        unknown = line
        return -1

# In[71]:

def get_unknown():
    global unknown
    return unknown

def menunumberExtract(pos):
    for keyword, type in pos:
        if type == 'MDN' or type == 'MDT':
            number.append(keyword)
    if len(number):
        return number[0]
    else :                    
        return -1


def get_intent(file_path):
    ret_str = transcribe_file(file_path)
    #print("PYTHON::ret_str : "  + str(ret_str))
    intent = analyze_intent(ret_str)
    #print("PYTHON::ret_str " + str(intent))
    return intent
