#coding=utf-8
import mysql.connector

class ConnectDB(object):

    def connectdb(self,host,user,password,database):
        conn = mysql.connector.connect(host=host,
                                       user=user,
                                       password=password,
                                       database=database)
        return conn

    def execselect(self,conn,sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        values = cursor.fetchall()
        for value in values:
            print value
        cursor.close()
        conn.close()

    def execother(self,conn,sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()


if __name__=='__main__':
    CN=ConnectDB()
    conn=CN.connectdb('10.12.13.171','credit2','Credit2Bank','yzxv4')
    CN.execselect(conn,'select * from t_general_code')
