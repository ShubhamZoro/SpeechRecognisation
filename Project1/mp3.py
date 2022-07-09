from pydub import AudioSegment
audio=AudioSegment.from_wav("DJ.wav")
audio=audio+6

audio=audio.fade_in(2000)
audio.export("mashup.mp3",format="mp3")
audio2=AudioSegment.from_mp3("mashup.mp3")
print("done")