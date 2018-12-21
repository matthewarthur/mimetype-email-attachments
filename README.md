# mimetype-email-attachments
extracting attachments from raw mimetype emails with base64-encoded attachments 

only tested with jpg but should work for any base64 attachment

see https://github.com/martysweet/aws-lambda-attachment-extractor/blob/master/lambda_email_extractor.py for a better implementation (that I couldn't get to work)


#ec2exec
ensure gh repo token is in ssm-parameter store. script location: {"owner":"matthewarthur", "repository": "mimetype-email-attachments", "path": "/test2execawslinux", "tokenInfo":"{{ssm-secure:gh-mattarthur-read}}" }
