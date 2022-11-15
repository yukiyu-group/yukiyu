# 该模块是用户管理模块
# 主要提供数据库中的用户管理功能
# 实现在数据库中进行用户创建、授权、修改、删除等具体操作
# 该模块实现的功能供user模块封装调用


import pymysql
import traceback
from pymysql import cursors
from werkzeug.security import check_password_hash, generate_password_hash
from itertools import chain
import config


# 默认创建普通用户，授权select
def createUser(name, password):
    returnStatus = 1
    db = pymysql.connect(
        host=config.host,
        port=config.port,
        db=config.database,
        user=config.user,
        password=config.password,
        charset='utf8')
    cursor = db.cursor()


    #查询是否存在
    cursor.execute("select name from user_list")
    elems = cursor.fetchall()
    res = list(chain.from_iterable(elems))
    print('现有用户：')
    print(res)
    if name in res:
        print("用户%s已存在" / (name))
        return -5

    # 插入新用户
    priv = 'YNNN'
    sql2 = """
    insert into user_list(name,password,privilege) 
    values
    ('%s','%s','%s');""" % \
           (name, generate_password_hash(password), priv)
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        db.commit()
        print('insert success !')
    except:
        print('insert error!')
        db.rollback()
        traceback.print_exc()
        returnStatus=0
        
    db.close()
    return returnStatus


# 删除用户
def dropUser(name):
    returnStatus = 1
    db = pymysql.connect(
        host=config.host, 
        port=config.port, 
        db=config.port, 
        user=config.user, 
        password=config.password,
        charset='utf8')
    cursor = db.cursor()

    sql2 = """
    delete from user_list
    where name = '%s';
    """ % \
           (name)
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        db.commit()
        print('delete user success !')
    except:
        print('delete user error!')
        db.rollback()
        traceback.print_exc()
        returnStatus = 0

    cursor.close()
    db.close()

    return returnStatus


def ifManage(name):
    db = pymysql.connect(
        host=config.host,
        port=config.port,
        db=config.database,
        user=config.user,
        password=config.password,
        charset='utf8')
    sql = """
        select if_manager 
        from user_list
        where name = '%s';
    """ % \
          (name)
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

    cursor.close()
    db.close()

    return data[0]['if_manager']


# 授权为管理员用户，实现所有权限
def grantSuperUser(name):
    if ifManage(name) == 'Y':
        print("success")
        return 1

    db = pymysql.connect(
        host=config.host,
        port=config.port,
        db=config.database,
        user=config.user,
        password=config.password,
        charset='utf8')
    cursor = db.cursor()
    sql2 = """
    update user_list
    set privilege = 'YYYY'
    where name = '%s';
    """%\
    (name)
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        db.commit()
        print('update success !')
    except:
        print('update error!')
        db.rollback()
        traceback.print_exc()
        return 0

    sql3 = """
        update user_list
        set if_manager = 'Y'
        where name = '%s';
    """ % \
           (name)
    try:
        print('start to execute:')
        print(sql3)
        cursor.execute(sql3)
        db.commit()
        print('update success !')
    except:
        print('update error!')
        db.rollback()
        traceback.print_exc()
        return 0

    cursor.close()
    db.close()
    return 1


# 授权为普通用户，select权限
def grantOrdinartUser(name):
    returnStatus = 1
    if (ifManage(name) == 'N'):
        print("grant success")
        return 1

    db = pymysql.connect(
        host=config.host,
        port=config.port,
        db=config.database,
        user=config.user,
        password=config.password,
        charset='utf8')
    cursor = db.cursor()

    sql2 = """
    update user_list
    set privilege = 'YNNN'
    where name = '%s';
    """ % \
           (name)
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        db.commit()
        print('update success !')
    except:
        print('update error!')
        db.rollback()
        traceback.print_exc()
        return 0

    sql3 = """
        update user_list
        set if_manager = 'N'
        where name = '%s';
    """ % \
           (name)
    try:
        print('start to execute:')
        print(sql3)
        cursor.execute(sql3)
        db.commit()
        print('update success !')
    except:
        print('update error!')
        db.rollback()
        traceback.print_exc()
        return 0

    changePrivilege(name, 'YYYY')

    cursor.close()
    db.close()
    return returnStatus



# 查询指定用户权限
def privilegeOfUser(name):
    db = pymysql.connect(
        host=config.host,
        port=config.port,
        db=config.database,
        user=config.user,
        password=config.password,
        charset='utf8')
    cursor = db.cursor(pymysql.cursors.DictCursor)
    sql = """
        select privilege
        from user_list
        where name = '%s';
    """%\
    (name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('success !')
    except:
        print('error!')
        traceback.print_exc()

    data = cursor.fetchall()
    print(data)

    dict = {'name': name,'privilege':data[0]["privilege"]}

    print(dict)
    return dict



# #查看所有用户及权限
# def privilegeOfAllUser():
#     db = pymysql.connect(
#         host=config.host, 
#         port=config.port, 
#         db="mysql", 
#         user=config.user, 
#         password=config.password,
#         charset='utf8')
#     cursor=db.cursor(pymysql.cursors.DictCursor)

#     sql = """
#         select User, select_priv, insert_priv, update_priv, delete_priv, create_priv, drop_priv
#         from db
#         where Db = 'yukiyu';
#     """
#     try:
#         print('start to execute:')
#         print(sql)
#         cursor.execute(sql)
#         print('success !')
#     except:
#         print('error!')
#         traceback.print_exc()

#     data = cursor.fetchall()
#     cursor.close()
#     db.close()
#     list = []
#     for item in data:
#         a=item['select_priv']
#         b=item['insert_priv']
#         c=item['update_priv']
#         d=item['delete_priv']
#         s=a+b+c+d
#         list.append({'name': item['User'],'privilege':s})


#     print(list)
#     return list

# def printAllUser():
#     db = pymysql.connect(
#         host=config.host, 
#         port=config.port, 
#         db="mysql", 
#         user=config.user, 
#         password=config.password,
#         charset='utf8')
#     cursor=db.cursor(pymysql.cursors.DictCursor)
#     sql = "select if_manager, user_id, name, privilege  from yukiyu.user_list;"
#     try:
#         print('start to execute:')
#         print(sql)
#         cursor.execute(sql)
#         print('success !')
#     except:
#         print('error!')
#         traceback.print_exc()
#     data = cursor.fetchall()
#     print(data)

#返回用户密码hash值
def getPassword(name):
    db = pymysql.connect(
        host=config.host, 
        port=config.port, 
        db=config.port, 
        user=config.user, 
        password=config.password,
        charset='utf8')
    cursor=db.cursor(pymysql.cursors.DictCursor)
    sql = "select password from user_list where name = '%s'"%\
        (name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('success !')
    except:
        print('error!')
        traceback.print_exc()
    
    data = cursor.fetchall()
    password_hash = data[0]['password']
    
    print(password_hash)
    return password_hash


def changePrivilege(name,priv):

    db = pymysql.connect(
        host=config.host,
        port=config.port,
        db=config.database,
        user=config.user,
        password=config.password,
        charset='utf8')
    cursor=db.cursor(pymysql.cursors.DictCursor)
    sql = """
    update user_list
    set privilege = '%s'
    where name = '%s';
    """%\
    (priv,name)
    try:
        print('start to execute:')
        print(sql)
        cursor.execute(sql)
        print('success !')
    except:
        print('error!')
        traceback.print_exc()
    
    cursor.close()
    db.close()
    
    return 1

    if priv[3] == 'Y':
        addPrivForUser(name, 'delete')
    else:
        delPrivForUser(name, 'delete')

    return 1


# 包装函数
# info中的password为明文密码
# info = ['Y',id,'name','password','priv']
def commmitChangeToUserlist(oldInfo, newInfo):
    db = pymysql.connect(
        host=config.host,
        port=config.port,
        db=config.database,
        user=config.user,
        password=config.password,
        charset='utf8')

    if oldInfo != None and newInfo != None:
        if oldInfo[0] == 'N' and newInfo[0] == 'Y':
            newInfo[4] = 'YYYY'
        if oldInfo[0] == 'Y' and newInfo[0] == 'Y' and newInfo[4] != 'YYYY':
            print('privilege error')
            return -4

    sql1 = "savepoint x;"
    cursor = db.cursor()
    cursor.execute(sql1)
    print(sql1)

    if oldInfo == None:
        print('insert')
        returnStatus = insertItem(newInfo)
    elif newInfo == None:
        print('delete')
        returnStatus = deleteItem(oldInfo)
    else:
        print('update')
        returnStatus = updateItem(newInfo, oldInfo)

    if (returnStatus != 1):
        print('error')
        sql2 = "rollback to x;"
        cursor.execute(sql2)
        db.commit()
        print(sql2)

    sql3 = "release savepoint x;"
    cursor.execute(sql3)
    db.commit()
    print(sql3)

    return returnStatus


# 插入新用户
def insertItem(newInfo):
    status = 1
    ifManage = newInfo[0]
    name = newInfo[2]
    password = newInfo[3]
    privilege = newInfo[4]

    status = createUser(name, password)
    if (status != 1):
        return status

    if (ifManage == 'Y'):
        status = grantSuperUser(name)
    else:
        status = grantOrdinartUser(name)

    if status != 1:
        return status

    status = changePrivilege(name, privilege)
    if status != 1:
        return status

    print('insert item success')
    return 1


# 删除某用户
def deleteItem(oldInfo):
    status = 1
    name = oldInfo[2]

    status = dropUser(name)

    if status == 0:
        print('delete item error')
        return 0

    print('delete item success')
    return status


# 更新信息

def updateItem(newInfo, oldInfo):
    returnStatus = 1

    nifManage = newInfo[0]
    nname = newInfo[2]
    npassword = newInfo[3]
    npriv = newInfo[4]

    oifManage = oldInfo[0]
    oname = oldInfo[2]
    opassword = oldInfo[3]
    opriv = oldInfo[4]

    if (npriv != opriv):
        returnStatus = changePrivilege(oname, npriv)
        if returnStatus != 1:
            print('change privilege error')
            return returnStatus
        print('change privilege success')
    if (nifManage != oifManage):
        returnStatus = changeIfManage(oname, nifManage)
        if returnStatus != 1:
            print('change ifManager error')
            return returnStatus
        print('change ifManager success')
    if (npassword != opassword):
        returnStatus = changePassword(oname, npassword)
        if returnStatus != 1:
            print('change password error')
            return returnStatus
        print('change password success')
    if (oname != nname):
        returnStatus = changeName(oname, nname)
        if returnStatus != 1:
            print('change name error')
            return returnStatus
        print('change name success')

    print('update item success')
    return returnStatus


# 用户改姓名
def changeName(oname, nname):
    returnStatus = 1
    db = pymysql.connect(
        host=config.host,
        port=config.port,
        db=config.database,
        user=config.user,
        password=config.password,
        charset='utf8')
    cursor = db.cursor()

    cursor.execute("select name from user_list")
    elems = cursor.fetchall()
    res = list(chain.from_iterable(elems))
    print('现有用户：')
    print(res)
    if nname in res:
        print("用户%s已存在" / (nname))
        return -5

    sql2="""
    update user_list 
    set name = '%s'
    where name = '%s';""" % \
           (nname, oname)
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        db.commit()
        print('success !')
        returnStatus = 1
    except:
        print('updata user error !')
        db.rollback()
        traceback.print_exception()
        returnStatus = 0
        return returnStatus

    return 1


# 用户改管理权限
def changeIfManage(name,nIfMnage):

    if (nIfMnage == 'Y'):
        returnStatus = grantSuperUser(name)
    else:
        returnStatus = grantOrdinartUser(name)
    return returnStatus


# 用户改密码
def changePassword(name, password):
    db = pymysql.connect(
        host=config.host,
        port=config.port,
        db=config.database,
        user=config.user,
        password=config.password,
        charset='utf8')
    cursor = db.cursor()

    password_hash = generate_password_hash(password)
    sql2 = """
    update yukiyu.user_list
    set password = '%s'
    where name = '%s';
    """ % \
           (password_hash, name)
    try:
        print('start to execute:')
        print(sql2)
        cursor.execute(sql2)
        db.commit()
        print('success !')
        returnStatus = 1
    except:
        print('updata error !')
        db.rollback()
        traceback.print_exception()
        returnStatus = 0

    db.close()
    return returnStatus


def test1():
    newInfo = ['N', 2, 'ddd', '123456', 'YNNN']
    commmitChangeToUserlist(None, newInfo)
    print('success')
    return


def test2():
    oldInfo = ['N', 2, 'ddd', '123456', 'YNNN']
    newInfo = ['Y', 2, 'ddd', '123456', 'YNNN']
    commmitChangeToUserlist(oldInfo, newInfo)


def test3():
    oldInfo = ['Y', 2, 'ddd', '123456', 'YYYY']
    newInfo = ['Y', 2, 'xx', '123456', 'YYYY']
    commmitChangeToUserlist(oldInfo, newInfo)


def test4():
    oldInfo = ['N', 2, 'xx', '123456', 'YNNN']
    commmitChangeToUserlist(oldInfo, None)


def test5():
    oldInfo = ['N', 2, 'xx', '123456789', 'YNNN']
    newInfo = ['Y', 2, 'xxyy', '123456789', 'YYYY']
    commmitChangeToUserlist(oldInfo, newInfo)


if __name__ == '__main__':
    # dropUser('xxy')
    # test1()
    # test2()
    test3()
    # test4()

    # test5()

    db = pymysql.connect(
        host=config.host,
        port=config.port,
        db=config.database,
        user=config.user,
        password=config.password,
        charset='utf8')
    # dropUser('xxx')
    # createUser('xxx','123456')
    # grantSuperUser('cy')
    # grantOrdinartUser('cyy')
    # addPrivForUser('cyy','delete')
    # delPrivForUser('cyy','delete')
    # privilegeOfAllUser()
    # privilegeOfUser('cyy')

    # printAllUser()
    # getPassword('xxx')

    db.close()
