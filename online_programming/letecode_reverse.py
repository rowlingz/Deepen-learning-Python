# -*- coding:utf-8 -*-
"""
题目背景：
给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。
假设我们的环境只能存储得下 32 位的有符号整数，则其数值范围为 [−2^31,  2^-31]。请根据这个假设，如果反转后整数溢出那么就返回 0。
"""


class Solution(object):

    def reversed_positive(self, x):
        """
        方法1：用数学的方式解决，余数 及整除 的定义
        :param x: 正整数
        :return:
        """
        rev = 0
        while x:
            pop = x % 10
            rev = rev * 10 + pop
            x //= 10
            if rev > 2147483647:
                return 0
        return rev

    def reversed_all(self, x):
        """
        所有整数反转
        :param x:
        :return:
        """
        if x >= 0:
            return self.reversed_positive(x)
        else:
            return -self.reversed_positive(-x)

    def reverse(self, x):
        """
        方式2：借助列表进行末尾弹出，列表拼接、类型转换等方式反转数字
        :type x: int
        :rtype: int
        """
        x_l = list(str(x))
        x_l_r = []
        lead_string = x_l[0]
        while x_l:
            x_l_r.append(x_l.pop())
        if lead_string == '-':
            x_r = -1 * int(''.join(x_l_r[:-1]))
        else:
            x_r = int(''.join(x_l_r))
        if x_r <= -2147483647 or x_r > 2147483647:
            return 0
        else:
            return x_r
