import pymysql
import config

def getRankList():
    db = pymysql.connect(
        host=config.host,
        port=config.port,
        db=config.database,
        user=config.user,
        password=config.password,
        charset='utf8')
    sql = """
        select bangumi_detail.title,play_url,heat,img
        from bangumi_detail inner join bangumi_list on bangumi_detail.bangumi_id=bangumi_list.bangumi_id  inner join bilibili on bangumi_detail.bangumi_id = bilibili.bangumi_id
        where heat > 0
        order by heat DESC;
    """
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        print('success !')
        print(data)
        print(type(data))
        print(type(data[0]))
    except:
        print('error!')
        traceback.print_exc()

    cursor.close()
    db.close()

    if(len(data)==0):
        return []
    return data

if __name__ == '__main__':
    getRankList()