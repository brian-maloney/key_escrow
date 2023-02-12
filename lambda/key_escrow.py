import boto3
import configparser
import io
import json
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

    if response['result'] == 'allow':
        response['key'] = s3.Object('vond-key-escrow', 'keys/' + request['key']).get()['Body'].read().decode('utf-8')

    return response
