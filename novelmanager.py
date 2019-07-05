import re
from utilities import txt_utilities as txtUtilities
from utilities.database_utilities import DatabaseUtilities
import txt_reader


dbFilePath = 'novels.db'
db = DatabaseUtilities(dbFilePath)


def getNovels():
    novels = db.findNovels()
    return novels


def get_paragraph(paragraphIdx):
    paragraphs = db.getParagraph(paragraphIdx)
    return paragraphs


def analysis_txt(filePath, lineSize, lineCount):
    with open(filePath, 'r', encoding='utf-8') as f:
        title = ''
        contents = []
        paragraphIdx = 1
        while True:
            line = f.readline()  # 逐行读取
            if not line:  # 到 EOF，返回空字符串，则终止循环
                break

            try:
                matchObj = re.match(r'(\S*序)|([正文]*\s*[第终][0123456789一二三四五六七八九十百千万零 　\s]*[章部集节卷]) \S*', line)

                if matchObj:
                    if contents and len(contents) > 0:
                        chapterId = db.save_chapter({'novelId': 1, 'title': title})
                        paragraphIdx = analysis_chapter(chapterId, contents, lineSize, lineCount, paragraphIdx)
                        paragraphIdx += 1
                    title = ''
                    contents = []

                    title = matchObj.group()
                    contents.append(line)
                else:
                    contents.append(line)
            except Exception as e:
                print(e)


def analysis_chapter(chapterId, contents, lineSize, lineCount, paragraphIdx):
    paragraphLines = []
    paragraphLine = ''
    paragraphSize = 0
    firstLine = True
    for lineContent in contents:
        for ch in lineContent:
            if ch == '\n':
                continue
            paragraphSize += txtUtilities.get_word_width(ch)
            if paragraphSize > lineSize-1:
                paragraphLines.append(paragraphLine)
                if len(paragraphLines) >= lineCount:
                    save_paragraph(chapterId, paragraphIdx, paragraphLines)
                    paragraphLines = []
                    paragraphIdx += 1
                paragraphLine = ch
                paragraphSize = txtUtilities.get_word_width(ch)
            else:
                paragraphLine += ch

        if paragraphLine != '':
            paragraphLines.append(paragraphLine)
            paragraphLine = ''
            paragraphSize = 0
            if firstLine:
                paragraphLines.append(' ')
                firstLine = False

            if len(paragraphLines) >= lineCount:
                save_paragraph(chapterId, paragraphIdx, paragraphLines)
                paragraphIdx += 1
                paragraphLines = []

    save_paragraph(chapterId, paragraphIdx, paragraphLines)
    return paragraphIdx


def save_paragraph(chapterId, paragraphIdx, paragraphLines):
    db.save_paragraph({'chapterId': chapterId, 'idx': paragraphIdx, 'content': '\n'.join(paragraphLines)})


def update_current_Paragraph(novelId, paragraphIdx):
    db.update_current_Paragraph(novelId, paragraphIdx)


if __name__ == '__main__':
    db.clear_novel(1)
    db.save_novel('诡秘之主')

    mainWinConfig = txt_reader.get_main_win_config()
    analysis_txt('/Users/zhusonghua/Documents/zhush/resource/ebooks/诡秘之主.txt', mainWinConfig['width']-4, mainWinConfig['height']-4)
