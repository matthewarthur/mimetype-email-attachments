from __future__ import print_function

import email
import zipfile
import os
import gzip
import string
import boto3
import urllib
import logging
import boto3
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
s3r = boto3.resource('s3')

def lambda_handler(event, context):

    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    logger.info('Reading {} from {}'.format(file_key, bucket_name))

    # Read the raw text file into a Email Object
    response = s3r.Bucket(bucket_name).Object(file_key)
    message = email.message_from_string(response.get()["Body"].read())


#pull the attachment and check the content type
#here's the place to add if / else logic to limit to particular attachment types
    attachment = message.get_payload()[1]
    attachment.get_content_type()
    contentdisp = str.split(attachment.get('Content-Disposition'), '=')  #grab attachment name
    fname = contentdisp[1].replace('\"', '')
#should probably write these to a /tmp/ directory then blow it away later
    tmpfname = 'tmp' + fname
    open('/tmp/' + tmpfname, 'w').write(attachment.get_payload())
    jpgtxttmp = open('/tmp/' + tmpfname,'rb').read().replace('\n','')   #strip whitespace
    processfname = 'prc' + fname

    jpgprocess = open('/tmp/' + processfname, 'w')   #open the stream for the tmp file
    jpgprocess.write(jpgtxttmp)    #write the temp flow to it
    jpgprocess.close()
    newjpgtxt = open('/tmp/' + processfname, 'rb').read()
    jpgprocessed = open('/tmp/' + fname, 'w')
    jpgprocessed.write(newjpgtxt.decode('base64'))     #write the decoded txt
    jpgprocessed.close()

#write to s3
    s3.upload_file('/tmp/' + fname, bucket_name, fname)

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda success!')
    }
