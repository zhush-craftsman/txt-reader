def zh2unicode(stri):
    """Auto converter encodings to unicode
        It will test utf8,gbk,big5,jp,kr to converter"""
    for c in ('utf-8', 'gbk', 'gb2312', 'jp', 'euc_kr', 'utf16', 'utf32'):
        try:
            return stri.decode(c)
        except Exception:
            pass
    return stri


def zh2utf8(stri):
    """Auto converter encodings to utf8
        It will test utf8,gbk,big5,jp,kr to converter"""
    for c in ('utf-8', 'gbk', 'big5', 'jp', 'euc_kr', 'utf16', 'utf32'):
        try:
            return stri.decode(c).encode('utf8')
        except Exception:
            pass
    return stri
