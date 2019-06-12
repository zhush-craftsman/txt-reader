import re
from utilities import txt_utilities as txtUtilities
from utilities.database_utilities import DatabaseUtilities


dbFilePath = 'novels.db'


def getNovels():
    db = DatabaseUtilities(dbFilePath)
    novels = db.findNovels()
    return novels


# 生成一个列表,记录了小说的所有章节,名字,bookid
def getList():
    # 生成一个总的列表,有所有章节,书号,书名
    novelList = open('novelList').read().split()
    if len(novelList) == 0:
        return []
    mlen = num = None
    # 处理显示,把标题长短 用空格替补 以用来对齐
    lenth = [len(novelList[2 * i + 1]) for i in range(len(novelList) // 2)]
    # lenth=[len(i[1]) for i in novelList]
    # 加判断 避免 lenth为0 max出错
    if len(lenth) > 0:
        mlen = max(lenth)

    nlist = []

    for i in range(len(novelList) // 2):
        # 为书名短的统一补上空格
        num = 2 * (mlen - lenth[i]) // 3
        temp = novelList[2 * i + 1] + num * ' '
        nlist.append(temp)

    return nlist


def read_book(novelId, lineRow, lineSize):
    db = DatabaseUtilities(dbFilePath)
    chapterId = 1
    while True:
        forward = None
        chapter = db.getChapter([chapterId])
        if not chapter:
            break

        title = chapter['title']
        content = title + '\n' + chapter['content']
        contentToLines = content.split('\n')
        if forward == -1:
            contentToLines.reverse()

        chapterIter = read_chapter(contentToLines, lineRow, lineSize, forward)
        while True:
            try:
                forward = yield chapterIter.send(forward)
            except StopIteration:
                break

        if forward == 1 or forward is None:
            chapterId += 1
        elif forward == -1:
            chapterId -= 1
        else:
            chapterId += 1

        if chapterId == 0:
            break


def read_chapter(contentToLines, lineRow, lineSize, forward):
    delLineCnt = 0
    lineList = []
    i = 0
    while i < len(contentToLines) and i >= 0:
        lineContent = contentToLines[i]
        if not lineContent:
            if forward == 1 or forward is None:
                i += 1
            elif forward == -1:
                i -= 1
            continue
        length = len(lineContent)

        startIndex = 0
        endIndex = lineSize if lineSize < length else length
        if forward == -1:
            startIndex = length-lineSize if length-lineSize > 0 else 0
            endIndex = length
        while endIndex <= length:
            subStr = lineContent[startIndex:endIndex]
            if delLineCnt == 0:
                lineList.append(subStr)
            else:
                delLineCnt -= 1

            if len(lineList) >= lineRow:
                if forward == -1:
                    lineList.reverse()
                newforward = yield lineList
                if forward is not None and newforward != forward:
                    delLineCnt = lineRow - 1
                forward = newforward
                lineList = []

            if (forward == 1 or forward is None) and endIndex == length:
                break
            elif forward == -1 and startIndex == 0:
                break

            if forward == 1 or forward is None:
                startIndex = endIndex
                endIndex = endIndex + lineSize if endIndex + lineSize < length else length
            elif forward == -1:
                endIndex = startIndex
                startIndex = endIndex - lineSize if endIndex - lineSize > 0 else 0

        if forward == 1 or forward is None:
            i += 1
        elif forward == -1:
            i -= 1

    if len(lineList) > 0:
        yield lineList


def splite_str(str, lineRow=15, lineSize=20):
    defaultLineSize = lineSize
    subStrs = str.split('\n')
    lineList = []
    lineListFull = False
    cnt = 0
    for i in range(len(subStrs)):
        subStr = subStrs[i]
        length = len(subStr)
        startIndex = 0
        endIndex = defaultLineSize-1 if defaultLineSize < length else length-1
        while (not lineListFull) and endIndex <= length-1:
            subSubStr = subStr[startIndex:endIndex]
            lineList.append(subSubStr)
            cnt += len(subSubStr.encode('gb2312'))
            if len(lineList) >= lineRow:
                lineListFull = True
            startIndex = endIndex
            endIndex = endIndex + defaultLineSize if endIndex + defaultLineSize < length else length
        if lineListFull:
            break
    return lineList, cnt


def contain_chapter_title(line):
    # if re.match(ur"[正文]*\s*[第终][0123456789一二三四五六七八九十百千万零 　\s]*[章部集节卷]", unicode(line,'utf-8')) :
    matchObj = re.match(r'[正文]*\s*[第终][0123456789一二三四五六七八九十百千万零 　\s]*[章部集节卷]', txtUtilities.zh2unicode(line))
    if matchObj:
        return True, matchObj.group(), line[matchObj.end():]
    else:
        return False


def analysis_txt(filePath):
    db = DatabaseUtilities(dbFilePath)

    with open(filePath, 'r', encoding='gb2312') as f:
        title = ''
        contents = []
        while True:
            line = f.readline()  # 逐行读取
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break

            try:
                matchObj = re.match(r'[正文]*\s*[第终][0123456789一二三四五六七八九十百千万零 　\s]*[章部集节卷]', txtUtilities.zh2unicode(line))

                if matchObj:
                    db.saveChapter({'novelId': 1, 'title': title, 'content': '\n'.join(contents)})
                    title = ''
                    contents = []

                    title = matchObj.group()
                    contents.append(line[matchObj.end():])
                else:
                    contents.append(line)
            except Exception as e:
                print(e)


def read_txt_in_chunks(filePath, chunk_size=1024 * 1024):
    '''
    # example: 将文档按块进行读取
    filePath = ''
    for chunk in read_txt_in_chunks(filePath):
        print(filePath)
    '''
    with open('filepath', 'r', encoding='utf-8') as f:
        while True:
            chunk_data = f.read(chunk_size)
            if not chunk_data:
                break
            yield chunk_data


if __name__ == '__main__':
    # analysis_txt('万历十五年_gb2312.txt')
    # print(getNovels())
    pass
