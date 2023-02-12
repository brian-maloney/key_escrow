import boto3
import configparser
import io
import json
from base64 import b64encode
import duo_client

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    config = configparser.RawConfigParser()

    config.read_file(io.StringIO(s3.Object('vond-key-escrow', 'duo.conf').get()['Body'].read().decode('utf-8')))

    auth_api = duo_client.Auth(
        ikey = config.get('duo', 'ikey'),
        skey = config.get('duo', 'skey'),
        host = config.get('duo', 'host'),
    )

    request = json.loads(event['body'])

    response = auth_api.auth(
        username=request['user'],
        device='auto',
        factor='push',
    )

    return_struct = {
        'statusCode': 200,
            'headers': {
                'Content-Type': ''
            },
            'body': '',
            'isBase64Encoded': False
    }


    if response['result'] == 'allow':
        obj = s3.Object('vond-key-escrow', 'keys/' + request['key']).get()
        return_struct['headers']['Content-Type'] = obj['ContentType']
        if obj['ContentType'].endswith('octet-stream'):
            return_struct['isBase64Encoded'] = True
            return_struct['body'] = b64encode(obj['Body'].read())
        else:
            return_struct['body'] = obj['Body'].read().decode('utf-8')

    else:
        return_struct['statusCode'] = 403
        return_struct['body'] = f"Disallowed due to response of type: {response['result']}\n"

    return return_struct
