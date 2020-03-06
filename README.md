# voice_snippets
为开源中文语音识别项目[asrt](https://github.com/nl8590687/ASRT_SpeechRecognition)开发的python客户端
GUI使用[PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)开发
## 功能
用户预先在客户端中定义key和value, 客户端录音后将音频信息通过http协议发给服务端, 接收服务端回复的拼音后与sqlite数据库的key进行匹配并输出相应value到剪贴板
## 依赖包
PySimpleGUI 4.13.1

PyAudio 0.2.11

pypinyin 0.36.0
## 运行
1.安装[asrt](https://github.com/nl8590687/ASRT_SpeechRecognition)的依赖

2.运行[asrt release](https://github.com/nl8590687/ASRT_SpeechRecognition/releases/download/v0.6.0/ASRT_v0.6.0.zip)release中的asrserver.py

3.运行本项目中的`main.py`

![](./picture/1.png)
