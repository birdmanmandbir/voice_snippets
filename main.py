import PySimpleGUI as sg
import sqlite3
import requests
from pinyin import get_pinyin
from clipboard import addToClipBoard
from get_audio import get_audio
import difflib


def get_equal_rate_1(str1, str2):
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()


class Evaluator:
    def __init__(self, pinyin_client: str, pinyin_server: str, content):
        self.content = content
        self.pinyin_client = pinyin_client
        self.pinyin_server = pinyin_server
        self.__score = 0
        self.get_score()

    # TODO maybe need to improve
    def get_score(self):
        self.__score += get_equal_rate_1(self.pinyin_server, self.pinyin_client)
        return self.__score

    def __eq__(self, other):
        return self.__score == other.__score

    def __lt__(self, other):
        return self.__score < other.__score

    def __str__(self):
        return 'score is {}'.format(self.__score)


url_server = "http://127.0.0.1:20000"
port = 20000
token_client = "qwertasd"
# database
conn = sqlite3.connect('test.db')
print("Opened database successfully")
c = conn.cursor()
c.execute('select CHARACTER,CONTENT from CORRES')
fetched_list = c.fetchall()
print(fetched_list)

# GUI
sg.change_look_and_feel('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
all_records = sg.Listbox(values=fetched_list, size=(30, 5))
layout = [[sg.Text('编辑常用语')],
          [sg.Text('Name'), sg.InputText()],
          [sg.Text('Content'), sg.InputText()],
          [sg.Submit(), sg.Button('Delete')],
          [all_records],
          [sg.Button('开始录音'), sg.Text('按下后记录4s语音')]
          ]

# Create the Window
window = sg.Window('语音识别常用语输入', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    # if event in (None, 'Cancel'):  # if user closes window or clicks cancel
    if event is None:  # if user closes window
        break
    elif event in '开始录音':
        sample_rate, wave_list = get_audio()
        print('record finnish')
        data_to_post = ''
        data_to_post += ('token=' + token_client)
        data_to_post += ('&fs={}'.format(sample_rate))
        for wave in wave_list:
            data_to_post += ('&w={}'.format(wave))
        # send request
        r = requests.post(url_server + '/post', data=data_to_post)
        print(r.content.decode(encoding='utf_8'))
        result_pinyin = r.content.decode(encoding='utf_8')
        server_pinyin = result_pinyin.split('&')
        c.execute('select PINYIN,CONTENT from CORRES')
        client_pinyins = c.fetchall()
        evaluators = []
        print(client_pinyins)
        for item in client_pinyins:
            client_pinyin = item[0].split('&')
            content = item[1]
            evaluators.append(Evaluator(client_pinyin, server_pinyin, content))
        for e in evaluators:
            print(e)
        evaluators.sort()

        result_content = evaluators[-1].content
        addToClipBoard(result_content)
        sg.PopupOK('成功输出到剪贴板')
    else:
        print('You entered ', values)
        character = values[0]
        pinyin_list = get_pinyin(character)
        pinyin = ''
        for pinyin_item in pinyin_list:
            pinyin += (pinyin_item[0] + '&')
        content = values[1]
        record = (character, pinyin, content)
        print(record)
        if event in ('Delete'):
            try:
                record_is_choose = values[2][0][0]
            except IndexError:
                continue
            print(record_is_choose)
            c.execute('DELETE FROM CORRES where CHARACTER = \'{}\''.format(record_is_choose))
        else:
            if character == '':
                continue
            try:
                c.execute('insert into CORRES values (?,?,?)', (character, pinyin, content))
            except sqlite3.IntegrityError:
                c.execute('DELETE FROM CORRES where CHARACTER = \'{}\''.format(character))
                c.execute('insert into CORRES values (?,?,?)', (character, pinyin, content))
                # sg.PopupOK('重复的项')
        conn.commit()
        c.execute('select CHARACTER,CONTENT from CORRES')
        fetched_list = c.fetchall()
        # print(fetched_list)
        all_records.Update(values=fetched_list)

c.close()
window.close()
