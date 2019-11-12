#-*- coding:utf-8 -*-

debug = True

import time
import datetime
import io

import os,sys

from flask import Flask, redirect, url_for, request,send_file

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types


import json

#########################################################

# [START speech_transcribe_sync]

def transcribe_file(speech_file):
    print(speech_file)
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
    print(os.getcwd())
    key_path = os.getcwd() + "/KEY/key.json"
    key_path = os.path.normpath(key_path)
#    input_path = os.getcwd() + "/output.wav"
    #input_path = os.getcwd() + file_name

    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     'speech_folder', help='Full path of audio file folder to be recognized')
    # args = parser.parse_args()
    # transcribe_file(args.speech_folder)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=key_path
    #print(input_path)
    kkma.pos(test[0])

    with open("config/inst.json") as json_file:
        json_data = json.load(json_file)
        names = json_data["name"]
        menus = json_data["menu"]


    print('NOTE::Python Module initialized')

########################################################

app = Flask(__name__)

@app.route('/speech',methods=['POST'])
def synth_call():
    print('speech call')
    file_path = request.form['path']
    #return get_intent(file_path)
    return transcribe_file(file_path)

@app.route('/text',methods=['GET'])
def text_call():
    print('text call')
    return unknown

@app.route('/')
def touch():
    print('touch')
    return 'hello from flask'


if __name__ == '__main__':
   init()
   #app.run(debug = True)
   # 모든 ip (외부 ip) 에서 접근 가능하도록 설정.
   #app.run(host='0.0.0.0',port = 1170)
   app.run(port = 1170)



