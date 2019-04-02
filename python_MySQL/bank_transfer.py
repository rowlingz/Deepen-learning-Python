# -*- coding:utf-8 -*-
# 银行转账是常用的事务操作案例，包含基本操作：
# 检查转入、
# 转出账户是否存在，
# 转出账户金额是否足够，
# 转出账户扣减金额，转入账户增加金额，转账过程结束。
import pymysql


class AccountRun:
    def __init__(self, conn):
        self.conn = conn

    def check_account(self, id):
        """检查账户是否存在"""
        cur = self.conn.cursor()
        sql_check = "select * from account where account_id = %s"

        try:
            cur.execute(sql_check, id)
            result_num = cur.rowcount
            if result_num != 1:
                raise Exception("账号%s不存在" % id)
        finally:
            cur.close()

    def check_money(self, id, money):
        """检查目标账户金额是否足够？"""
        cur = self.conn.cursor()

        sql_check_money = "select * from account where account_id = %s and money >= %s"
        try:
            cur.execute(sql_check_money, (id, money))
            result_num = cur.rowcount
            if result_num != 1:
                raise Exception("目标账户%s目前金额不足%s元" % (id, money))
        finally:
            cur.close

    def reduce_money(self, id, money):
        """扣除目标账户中的钱"""
        cur = self.conn.cursor()
        sql_add = "update account set money= money - %s where account_id = %s"
        try:
            cur.execute(sql_add, (money, id))
        except Exception as e:
            raise Exception('扣款失败', e)
        finally:
            cur.close

    def add_money(self, id, money):
        """给目标账户赚钱"""
        cur = self.conn.cursor()
        sql_add = "update account set money= money + %s where account_id = %s"
        try:
            cur.execute(sql_add, (money, id))
        except Exception as e:
            raise Exception('到账失败', e)
        finally:
            cur.close

    def transfer(self, source_id, target_id, money):
        try:
            self.check_account(source_id)
            self.check_account(target_id)
            self.check_money(source_id, money)
            self.reduce_money(source_id, money)
            self.add_money(target_id, money)
            self.conn.commit()
            print("转账成功")
        except Exception as e:
            self.conn.rollback()
            raise e


if __name__ == "__main__":
    source_id = input("请输出汇款账户： ")
    target_id = input("请输出目标账户： ")
    money = input("请输出转账金额: ")
    conn = pymysql.connect(host='localhost',
                           port=3306,
                           user='root',
                           password='root',
                           database='njust',
                           charset='utf8')
    tr_money = AccountRun(conn)
    try:
        tr_money.transfer(source_id, target_id, money)
    except Exception as e:
        print("转账失败", e)
    finally:
        conn.close()
