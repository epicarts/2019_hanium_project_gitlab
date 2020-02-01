import boto3

def imboto(message, username):
    polly_client = boto3.Session(
                aws_access_key_id='AKIA4I6N7T6BOAUIIVYQ',                     
    aws_secret_access_key='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',
    region_name='us-west-2').client('polly')

    response = polly_client.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3', 
                Text = message)
    response
    file = open('./uploads/' + username+'.mp3', 'wb+')
    file.write(response['AudioStream'].read())
    file.close()
