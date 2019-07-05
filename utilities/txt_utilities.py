zh_punc = "！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if '\u4e00' <= uchar <= '\u9fa5' or zh_punc.find(uchar):
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if '\u0030' <= uchar <= '\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if ('\u0041' <= uchar <= '\u005a') or ('\u0061' <= uchar <= '\u007a'):
        return True
    else:
        return False


def get_word_width(check_char):
    for ch in check_char:
        if is_chinese(ch):
            return 2
        else:
            return 1


if __name__ == '__main__':
    print(get_word_width('，'))
