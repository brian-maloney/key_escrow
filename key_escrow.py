import boto3
import ConfigParser
import StringIO
import duo_client

def lambda_handler(event, context):

    s3 = boto3.resource('s3')

    config = ConfigParser.RawConfigParser()

    config.readfp(StringIO.StringIO(s3.Object('yourbucketname', 'duo.conf').get()['Body'].read()))

    auth_api = duo_client.Auth(
        ikey = config.get('duo', 'ikey'),
        skey = config.get('duo', 'skey'),
        host = config.get('duo', 'host'),
    )

    response = auth_api.auth(
        username=event['user'],
        device='auto',
        factor='push',
    )

    if response['result'] == 'allow':
        response['key'] = s3.Object('yourbucketname', 'keys/' + event['key']).get()['Body'].read()

    return response
