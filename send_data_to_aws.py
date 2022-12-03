from flask import Flask, render_template, request
from botocore.exceptions import ClientError
from flask import render_template_string
import time
import boto3
import mutagen
from mutagen.mp3 import MP3
import os


app = Flask(__name__)

msg = None
s3 = boto3.resource('s3')
BUCKET_NAME='abnoamriha56143-mp3'
s3_1 = boto3.client('s3')
@app.route('/')  
def home():
    return render_template("file_upload_to_s3.html")

@app.route('/upload',methods=['post','get'])
def upload():
    global msg
    if request.method == 'POST':
        f = request.files['file']
        if f:   
            f.save(f.filename)
            if (f.headers.get('Content-Type') == 'audio/mpeg'):
                audio = MP3(f.stream)
                if(os.stat(f.filename).st_size != 0 and audio.info.length < 630):
                    s3_1.upload_file(f.filename, BUCKET_NAME, 'input.mp3')
                    msg = "Upload Done !"
                    if ((msg != "Please select a valid mp3 file") and (msg!= "Please upload a mp3 file format") and (msg != "Please upload a mp3 file that is shorter than 10 minutes") and (msg != None)):
                        print('Requesting summary of output ...')
                        if request.method == 'POST':
                            val = True
                            while val:
                                try:
                                    time.sleep(30)
                                    s3_object = s3.Bucket('abnoamriha56143-txt').Object('output.txt').get()
                                    msg = s3_object['Body'].read().decode('ascii')
                                    val = False
                                except ClientError as ex:
                                    print('No such key found')
                            if(len(msg) != 0):
                                text1 = msg.replace("/", "").replace('"', "").split(r'\n')
                                text2 = "<strong>" + "Sentiment : " + "</strong>" + text1[0] + '<br>' + "<strong>" + "Summary : " + "</strong>" + text1[1] 
                                msg = text2
                            else:
                                msg = 'Something went wrong. Please try again with another file'
                    
                else:
                    msg = "Please upload a mp3 file that is shorter than 10 minutes"
            else:
                msg = "Please upload a mp3 file format"
        else:
            msg = "Please select a valid mp3 file"
            return render_template("file_upload_to_s3.html", msg = msg)
    delete_buckets() 
    return render_template("file_upload_to_s3.html", msg = msg)


def delete_buckets():
    bucket1 = s3.Bucket('abnoamriha56143-mp3')
    bucket1.objects.all().delete()
    bucket2 = s3.Bucket('abnoamriha56143-json')
    bucket2.objects.all().delete()
    bucket3 = s3.Bucket('abnoamriha56143-txt')
    bucket3.objects.all().delete()   


 

if __name__ == "__main__":
    
    app.run(debug=True)
