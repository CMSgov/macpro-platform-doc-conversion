# This script assumes an API Gateway endpoint secured with an IAM resource policy
import requests
import base64
import json
import argparse
import ssl
print("\n\n\nCustom domain deployed from this repo requires TLS 1.2 or higher.")
print("We must be at openssl version 1.0.1 or higher to get TLS 1.2")
print("your version of SSL: ", ssl.OPENSSL_VERSION, "\n\n\n")

# note that this line will fail if you do not have botocore installed
# botocore installation instructions available here:
# https://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth


parser = argparse.ArgumentParser()
parser.add_argument("api_endpoint", help="https://<API ID>.execute-api.us-east-1.amazonaws.com/<branch name>/prince")
parser.add_argument("output_location", help="example: ~/Desktop")
args = parser.parse_args()
api_endpoint = args.api_endpoint
output_location = args.output_location
stage = api_endpoint.split('/')[-2]

# execute-api.<aws region>.amazonaws.com
aws_host = api_endpoint.split('/')[-3]



# Using aws-request-auth to AWS with Amazon's v4 signing process.
# aws-request-auth: https://github.com/DavidMuller/aws-requests-auth
# https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html
# Alternative packages or homemade is also possible

# We are using botocore here to dynamically pull AWS creds from any number of places
# Env vars, profile, IAM role, etc. Thus we can run this locally, in ec2, ECS, etc.
auth = BotoAWSRequestsAuth(
                           aws_host=aws_host,
                           aws_region='us-east-1',
                           aws_service='execute-api')


# latin-1 is required or we won't be able to decode this properly later
html_data = open("examples/test_data/test.html", "r", encoding="latin-1").read()

# str -> bytes
input_bytes = html_data.encode()


# bytes -> base64
b64_data = base64.b64encode(input_bytes)

print(f"508 html being converted to pdf:\n\n\n{html_data}\n\n\n")
print(f"sending request to {api_endpoint}:")
  

# Sending post request and saving response as response object
# Pass v4 signed request via auth object
r = requests.post(url = api_endpoint, data = b64_data, auth=auth)


# resp is json with base64 payload
api_resp = r.json()
# print(r.content)
print(r.json)

# base64 -> bytes
out_bytes = base64.b64decode(api_resp, validate=True)



# Perform a basic validation to make sure that the result is a valid PDF file
# Note this is not 100% reliable (the magic number / file signature)
if out_bytes[0:4] != b'%PDF':
  raise ValueError('Missing the PDF file signature')
 


# Write the PDF contents (bytes) to a local file
# b = binary
output_file = f'{output_location}/prince-{stage}.pdf'
f = open(output_file, 'wb')
f.write(out_bytes)
f.close()
print(f"508 PDF written to: {output_file}")
