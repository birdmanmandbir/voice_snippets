# -*- coding：utf-8 -*-
# -*- author：zzZ_CMing  CSDN address:https://blog.csdn.net/zzZ_CMing
# -*- 2018/07/12; 15:19
# -*- python3.5
import pyaudio
import wave
from scipy.io import wavfile
import numpy as np

input_filename = "input.wav"  # 麦克风采集的语音输入
input_filepath = "audios/"  # 输入文件的path
in_path = input_filepath + input_filename


def get_audio():
    filepath = in_path
    # aa = str(input("是否开始录音？   （y/n）"))
    # if aa == str("y") :
    CHUNK = 256
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  # 声道数
    RATE = 16000  # 采样率
    RECORD_SECONDS = 4
    WAVE_OUTPUT_FILENAME = filepath
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("*" * 10, "开始录音：请在{}秒内输入语音".format(RECORD_SECONDS))
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("*" * 10, "录音结束\n")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    sample_rate, sig = wavfile.read(in_path)
    # print("采样率: %d" % sample_rate)
    return sample_rate, sig
    # print(sig.tolist())
    # elif aa == str("n"):
    #     exit()
    # else:
    #     print("无效输入，请重新选择")
    #     get_audio(in_path)


# 联合上一篇博客代码使用，就注释掉下面，单独使用就不注释
# sample_rate, sig = wavfile.read(in_path)
# print("采样率: %d" % sample_rate)
# print(sig.tolist())
# https://blog.csdn.net/huplion/article/details/81040734
# if sig.dtype == np.int16:
#     print("PCM16位整形")
# if sig.dtype == np.float32:
#     print("PCM32位浮点")
