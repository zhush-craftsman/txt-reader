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
        # 获取游标
        _cursor = self._connection.cursor()
        # 执行SQL获取结果
        _cursor.execute(sql, args)
        if commit:
            self._connection.commit()
        data = _cursor.fetchall()
        _cursor.close()
        return data

    def saveNovel(self, novel):
        self.execute('insert into novel(name) values(?);', [novel])

    def saveChapter(self, chapter):
        self.execute('insert into chapter(novel_id, title, content) values(?, ?, ?);', [chapter['novelId'], chapter['title'], chapter['content']])

    def findNovels(self):
        return self.execute('select * from novel;')

    def getChapter(self, chapterId=0):
        return self.execute('select * from chapter where id = ?;', chapterId)[0]


if __name__ == '__main__':
    db = DatabaseUtilities('novels.db')

    db.execute('create table novel (id INTEGER not null primary key AUTOINCREMENT, name TEXT not null);')
    db.execute('create table chapter (id INTEGER not null primary key AUTOINCREMENT, novel_id INTEGER not null, title TEXT not null, content TEXT not null);')
