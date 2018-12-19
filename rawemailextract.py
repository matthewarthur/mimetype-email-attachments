#grab file from s3
#define your bucket as environmental variable
import boto3
import botocore

KEY = 'emailtestfile' # replace with your object key
s3 = boto3.resource('s3')

try:
    s3.Bucket(bucket).download_file(KEY, 'emailtestfile')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise

#the email package is part of python
#import to ingest the raw email and check if there are attachments
import email
import base64
import string   

message = email.message_from_file(open('emailtestfile'))
len(message.get_payload())

#pull the attachment and check the content type
#here's the place to add if / else logic to limit to particular attachment types
attachment = message.get_payload()[1]
#print the base64 encoded attachment
print(attachment)

attachment.get_content_type()
contentdisp = str.split(attachment.get('Content-Disposition'), '=')  #grab attachment name
fname = contentdisp[1].replace('\"', '')
print(fname)

#one file per step helps prevent buffer errors
#this could be improved!
#should probably write these to a /tmp/ directory then blow it away later
tmpfname = 'tmp' + fname
open(tmpfname, 'w').write(attachment.get_payload())
#print(tmpfname)
jpgtxttmp = open(tmpfname,'rb').read().replace('\n','')   #strip whitespace

processfname = 'prc' + fname
jpgprocess = open(processfname, 'w')   #open the stream for the tmp file
#print(processfname)
jpgprocess.write(jpgtxttmp)    #write the temp flow to it
jpgprocess.close()

newjpgtxt = open(processfname, 'rb').read()

jpgprocessed = open(fname, 'w')
#print(fname)
jpgprocessed.write(newjpgtxt.decode('base64'))     #write the decoded txt
jpgprocessed.close()


#write to s3
s3.Object(bucket, '<file>.jpeg').upload_file('/home/../../<file>.jpeg')

#clean up
import os
os.remove(processfname)
os.remove(tmpfname)
