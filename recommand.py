from random import choice
from itertools import chain
import MySQLdb

def recommand(user_id):
    # 创建连接数据库的对象  本地主机     用户    密码     数据库名称
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="recommand")
    '''
    Unix Socket vs TCP/IP: 当你使用 localhost 作为主机名时，
    MySQL客户端会尝试通过Unix套接字连接到MySQL服务器，
    而不是使用TCP/IP。而当你使用 127.0.0.1 时，
    它会强制使用TCP/IP连接。如果Unix套接字没有配置正确或存在问题，
    使用 127.0.0.1 会绕过这个问题。
    '''
    # 获取处理数据的游标，就是和数据库沟通的工具
    cursor = db.cursor()

    # 已经看过的最喜爱的番剧ID的SQL查询语句
    sql = "SELECT anime_id FROM user_anime WHERE user_id = {}".format(user_id)
    # 执行该语句，这时cursor就用上了
    cursor.execute(sql)

    # 获取最喜欢的番剧ID列表，chain方法可以接收任意数量的可迭代对象作为参数
    # 将全部参数中的元素去除，变成array放在迭代器中返回
    love_anime_id_list = list(chain(*cursor.fetchall()))
        # fetchall是cursor执行刚才查询语句后返回的所有结果，通常是元组
        # *就是解包，把tuple的元素拆成独立的
        # chain将其返回成新的迭代器，最后转换成list 例如，从[(1,), (2,), (3,)]，你会得到[1, 2, 3]。
    
    # 查询前三个最喜欢的番剧类型，数量
    sql = '''
            SELECT style_id, COUNT(style_id) FROM (
                SELECT style_id FROM anime_style WHERE anime_id IN(
                    SELECT anime_id FROM user_anime WHERE user_id = {}
                )
            )
            AS a GROUP BY 1 ORDER BY 2 DESC LIMIT 3;
          '''.format(user_id)
    cursor.execute(sql)
    
    # get前三个最喜欢的番剧类型及其数量
    love_style = cursor.fetchall()
    # 存储最喜欢的番剧类型ID及对应ID列表
    anime_dict = {}
    for (style_id, _) in love_style:
        sql = 'SELECT anime_id FROM anime_style WHERE style_id = {}'.format(style_id)
        cursor.execute(sql)
        anime_dict[str(style_id)] = [i[0] for i in cursor.fetchall()]

    # 喜欢的番剧ID集合
    whole_love_anime_id_set = set(chain(*anime_dict.values()))

    # 从喜欢的ID里移除已经看过的ID，剩下的就是喜欢但没看过的ID
    # 这部分就是潜在推荐内容
    unlook_love_anime_id_set = whole_love_anime_id_set.difference(set(love_anime_id_list))

    # 随机获取一个，即随机推荐一个
    random_anime_id = choice(list(unlook_love_anime_id_set))
    # 获取番剧名称及其简介的SQL
    sql = "SELECT name, brief FROM anime WHERE id = {}".format(random_anime_id)
    cursor.execute(sql)

    name, brief = cursor.fetchall()[0]
    result = {'name': name, 'brief': brief}
    db.close()
    return result

if __name__ == '__main__':
    print(recommand(1))