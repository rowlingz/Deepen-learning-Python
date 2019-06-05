# -*- coding:utf-8 -*-

# 编写一个程序判断给定的数是否为丑数。
# 丑数就是只包含质因数 2, 3, 5 的正整数。

# 1 是丑数。
# 输入不会超过 32 位有符号整数的范围: [−231,  231 − 1]。


# 执行用时 : 44 ms, 在Ugly Number的Python3提交中击败了99.20% 的用户
# 内存消耗 : 13.2 MB, 在Ugly Number的Python3提交中击败了77.87% 的用户

class Solution:
    def isUgly(self, num):
        if num <= 0:
            return False

        while num % 5 == 0:
            num = num / 5
        while num % 3 == 0:
            num = num / 3
        while num % 2 == 0:
            num = num / 2

        print(num)
        if num == 1:
            return True
        else:
            return False



s = Solution()
nums = [0, 6, 8, 14, 25, 30]
for num in nums:
    s.isUgly(num)

