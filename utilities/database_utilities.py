import sqlite3 as lite


class DatabaseUtilities:
    """
    sqlite数据库操作工具类
    database: 数据库文件地址，例如：db/mydb.db
    """
    _connection = None

    def __init__(self, database):
        # 连接数据库
        self._connection = lite.connect(database)

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def execute(self, sql, args=[], result_dict=True, commit=True) -> list:
        """
        执行数据库操作的通用方法
        Args:
        sql: sql语句
        args: sql参数
        result_dict: 操作结果是否用dict格式返回
        commit: 是否提交事务
        Returns:
        list 列表，例如：
        [{'id': 1, 'name': '张三'}, {'id': 2, 'name': '李四'}]
        """
        if result_dict:
            self._connection.row_factory = self._dict_factory
        else:
            self._connection.row_factory = None

        try:
            # 获取游标
            _cursor = self._connection.cursor()
            # 执行SQL获取结果
            _cursor.execute(sql, args)
            if commit:
                self._connection.commit()
            data = _cursor.fetchall()
            if not data:
                data = _cursor.lastrowid
            _cursor.close()
            return data
        except Exception as e:
            print(e)
            # pass

    def save_novel(self, novel):
        return self.execute('insert into novel(id, name) values(?, ?);', [1, novel])

    def save_chapter(self, chapter):
        return self.execute('insert into chapter(novel_id, title) values(?, ?);', [chapter['novelId'], chapter['title']])

    def save_paragraph(self, paragraph):
        return self.execute('insert into paragraph(chapter_id, idx, content) values(?, ?, ?);', [paragraph['chapterId'], paragraph['idx'], paragraph['content']])

    def clear_novel(self, novelId):
        self.execute('delete from novel')
        self.execute('delete from chapter')
        self.execute('delete from paragraph')

    def findNovels(self):
        return self.execute('select * from novel;')

    def getChapter(self, chapterId=0):
        return self.execute('select * from chapter where id = ?;', chapterId)[0]

    def getParagraph(self, paragraphIdx=0):
        return self.execute('select * from paragraph where idx = ?;', [paragraphIdx])[0]

    def update_current_Paragraph(self, novelId, paragraphIdx=0):
        return self.execute('update novel set current_paragraph_idx = ? where id = ?;', [paragraphIdx, novelId])


if __name__ == '__main__':
    db = DatabaseUtilities('novels.db')

    db.execute('create table novel (id INTEGER not null primary key AUTOINCREMENT, name TEXT not null, current_paragraph_idx INTEGER);')
    # db.execute('create table chapter (id INTEGER not null primary key AUTOINCREMENT, novel_id INTEGER not null, title TEXT not null);')
    # db.execute('create table paragraph (id INTEGER not null primary key AUTOINCREMENT, chapter_id INTEGER not null, idx INTEGER not null, content TEXT not null);')
