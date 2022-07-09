import os
import requests
import time
filename = "DJ.wav"
upload_endpoint='https://api.assemblyai.com/v2/upload'
transcript_endpoint="https://api.assemblyai.com/v2/transcript"
headers = {'authorization': f"{os.environ['secret_key']}"}
def upload():
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data


    response = requests.post(upload_endpoint,
                            headers=headers,
                            data=read_file(filename))

    audio_url=response.json()['upload_url']
    return audio_url

# transcription

def transcription(url):
    json = {
        "audio_url": url
    }

    trans_response = requests.post("https://api.assemblyai.com/v2/transcript", json=json, headers=headers)
    return trans_response.json()['id']



#poll

def poll(transcript_id):
    polling_endpoint = transcript_endpoint + "/" + transcript_id
    response=requests.get(polling_endpoint,headers=headers)
    return response.json()
def get_transcription_url(url):
    transcript_id=transcription(url)
    while True:
        response=poll(transcript_id)
        if response['status']=='completed':
            return response,None
        elif response['status']=='error':
            return response ,response["error"]

        print("waiting for 30 seconds")
        print(response['status'])
        print(response['text'])
        time.sleep(30)


def save_transcript(url,title):
    data, error = get_transcription_url(url)

    if data:
        filename = title + '.txt'
        with open(filename, 'w') as f:
            f.write(data['text'])
        print('Transcript saved')
    elif error:
        print("Error!!!", error)

url_=upload()
save_transcript(url_,"title")