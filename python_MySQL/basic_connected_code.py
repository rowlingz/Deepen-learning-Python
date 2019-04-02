# -*- coding:utf-8 -*-

import pymysql


# 数据库连接
def connect():
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='root',
                           database='njust',
                           charset='utf8')

    # 获取操作游标
    cursor = conn.cursor()
    return {"conn": conn, "cursor": cursor}


# 1、查询操作并打印结果
def select_sql(table):
    connection = connect()
    conn, cursor = connection['conn'], connection['cursor']
    sql = "select * from %s" % table
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()


# 插入操作
def insert_sql(persons_values):
    connection = connect()
    conn, cursor = connection['conn'], connection['cursor']

    keys = ", ".join(persons_values.keys())
    qmark = ", ".join(["%s"] * len(persons_values))
    sql_insert = "insert into persons(%s) values (%s)" % (keys, qmark)
    print(sql_insert)
    try:
        cursor.execute(sql_insert, list(persons_values.values()))
        conn.commit()
        print("插入成功")
    except Exception as e:
        print(e)
        conn.rollback()
        print("插入失败")
    finally:
        cursor.close()
        conn.close()


# 利用字典进行插入
def insert_sql2(message):
    connection = connect()
    conn, cursor = connection['conn'], connection['cursor']

    sql_insert = "insert into persons(ID, LastName, FirstName) " \
                 "values (%(ID)s, %(LastName)s, %(FirstName)s)"
    try:
        cursor.execute(sql_insert, message)
        conn.commit()
        print("插入成功")
    except Exception as e:
        print(e)
        conn.rollback()
        print("插入失败")
    finally:
        cursor.close()
        conn.close()


# 更新数据库
def update_sql():
    connection = connect()
    conn, cursor = connection['conn'], connection['cursor']

    sql_update = "update persons set birthday=%s where ID=%s"
    try:
        cursor.execute(sql_update, ('2001/7/5', 3))
        conn.commit()
        print('更新成功')
    except Exception as e:
        print('更新失败', e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
    pass


# 删除操作
def delete_sql(lastname):
    connection = connect()
    conn, cursor = connection['conn'], connection['cursor']

    sql_delete = "delete from persons where LastName=%s"
    try:
        cursor.execute(sql_delete, lastname)
        conn.commit()
        print('删除成功')
    except Exception as e:
        print('删除失败', e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
    pass


if __name__ == "__main__":

    persons_values = {
        "ID": 5,
        "LastName": "liy",
        "FirstName": "kity",
        "Address": "changan",
        "City": "jaingxi",
    }

    message = {
        "ID": 7,
        "LastName": "Jone",
        "FirstName": "Bob",
        "City": 'beijing'
    }

    insert_sql2(message)
    # update_sql()
    # delete_sql(lastname='Jone')


