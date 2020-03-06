from pypinyin import pinyin, Style
def get_pinyin(chars):
    return pinyin(chars, style=Style.TONE3, heteronym=False)