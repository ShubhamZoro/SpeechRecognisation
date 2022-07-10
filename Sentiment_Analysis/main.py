import os
import requests
import time
import json
filename = "DJ.wav"
upload_endpoint='https://api.assemblyai.com/v2/upload'
transcript_endpoint="https://api.assemblyai.com/v2/transcript"
headers = {'authorization': "d362826cc65f4b97bff735427da5b001"}
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

def transcription(url,sentiment_analysis):
    json = {
        "audio_url": url,
        'sentiment_analysis':sentiment_analysis
    }

    trans_response = requests.post("https://api.assemblyai.com/v2/transcript", json=json, headers=headers)
    return trans_response.json()['id']



#poll

def poll(transcript_id):
    polling_endpoint = transcript_endpoint + "/" + transcript_id
    response=requests.get(polling_endpoint,headers=headers)
    return response.json()
def get_transcription_url(url,sentiment_analysis):
    transcript_id=transcription(url,sentiment_analysis)
    while True:
        response=poll(transcript_id)
        if response['status']=='completed':
            return response,None
        elif response['status']=='error':
            return response ,response["error"]

        print("waiting for 30 seconds")
        # print(response['status'])
        # print(response['text'])
        time.sleep(30)


def save_transcript(url,title,sentiment_analysis=False):
    data, error = get_transcription_url(url,sentiment_analysis)

    if data:
        filename = title + '.txt'
        with open(filename, 'w') as f:
            f.write(data['text'])
        if sentiment_analysis:
            filename=title+'_sentiments.json'
            with open(filename,'w') as f:
                sentiments=data["sentiment_analysis_results"]
                json.dump(sentiments,f,indent=4)
        print('Transcript saved')
    elif error:
        print("Error!!!", error)

# url_=upload()
# save_transcript(url_,"title",sentiment=False)