import wave
obj=wave.open("01-basics_output.wav","rb")
print("Number of channels",obj.getnchannels())
print("Width",obj.getsampwidth())
print("Frame Rate",obj.getframerate())
print("Number of Frames",obj.getnframes())
print("Parameters",obj.getparams())
t_audio=obj.getnframes()//obj.getframerate()
print(f"Length of Audio File is {t_audio} sec")

frames=obj.readframes(-1)#-1 to reach all frames
print(type(frames),type(frames[0]))
print(len(frames))
obj.close()

obj_new=wave.open("Shubham.wav","wb")
obj_new.setnchannels(1)
obj_new.setsampwidth(2)
obj_new.setframerate(16000)
obj_new.writeframes(frames)
obj_new.close()
