# -*- coding:utf-8 -*-

# 判断一个整数是否是回文数。回文数是指正序（从左向右）和倒序（从右向左）读都是一样的整数。


class Solution:
    def isPalindrome(self, x):
        return str(x) == str(x)[::-1]


if __name__ == "__main__":
    s = Solution()
    x = 0
    print(s.isPalindrome(x))







