import pymysql
import config

def getDetailById(bangumiId):
    db = pymysql.connect(
        host=config.host,
        port=config.port,
        db=config.database,
        user=config.user,
        password=config.password,
        charset='utf8')
    sql = """
        select bangumi_id , description,actor,staff,title,heat
        from bangumi_detail
        where bangumi_id = '%s';
    """ % \
          (bangumiId)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        print('success !')
        print(data)
    except:
        print('error!')
        traceback.print_exc()



    sql = """
        select plays , follows
        from bilibili
        where bangumi_id = '%s';
    """ % \
          (bangumiId)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        data2 = cursor.fetchall()
        print('success !')
        print(data2)
    except:
        print('error!')
        traceback.print_exc()

    cursor.close()
    db.close()

    if(len(data)==0):
        return {}
    data = data[0]
    if(len(data2)==0):
        data['plays']=None
        data['follows']=None
        return data

    data2 = data2[0]

    data['plays']=data2['plays']
    data['follows']=data2['follows']
    return data