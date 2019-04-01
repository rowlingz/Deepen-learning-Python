# -*- coding:utf-8 -*-


import pymysql
from douban import settings


MYSQL_HOST = settings.MYSQL_HOST
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB


conn = pymysql.connect(host=MYSQL_HOST,
                       port=MYSQL_PORT,
                       user=MYSQL_USER,
                       password=MYSQL_PASSWORD,
                       database=MYSQL_DB,
                       charset='utf8',)
cursor = conn.cursor()


class Sql:

    # @classmethod
    # def insert_dd_name(cls, serial_number, movie_name, introduce, star, evaluate, m_describe):
    #     sql = "INSERT INTO top250movies(serial_number, movie_name, introduce, star, evaluate, m_describe) " \
    #           "VALUES (%(serial_number)s, %(movie_name)s, %(introduce)s, %(star)s, %(evaluate)s, %(m_describe)s)"
    #     value = {
    #         'm_describe': m_describe,
    #         'evaluate': evaluate,
    #         'introduce': introduce,
    #         'movie_name': movie_name,
    #         'serial_number': serial_number,
    #         'star': star,
    #     }
    #     cursor.execute(sql, value)
    #     conn.commit()

    @classmethod
    def insert_dd_name(cls, movies):
        keys = ", ".join(movies.keys())
        qmark = ", ".join(["%s"] * len(movies))
        sql = "INSERT INTO top250movies(%s) VALUES (%s)" % (keys, qmark)

        cursor.execute(sql, list(movies.values()))
        conn.commit()
