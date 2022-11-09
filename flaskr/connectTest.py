import pymysql
import config

#pymysql.connect(**config.configInfo)
db = pymysql.connect(
        host=config.host, 
        port=config.port, 
        db=config.database, 
        user=config.user, 
        password=config.password,
        charset='utf8')

db.close()