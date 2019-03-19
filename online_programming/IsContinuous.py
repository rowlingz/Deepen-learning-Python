# -*- coding:utf-8 -*-
# 题目背景
# LL今天心情特别好,因为他去买了一副扑克牌,发现里面居然有2个大王,2个小王(一副牌原本是54张^_^)...
# 他随机从中抽出了5张牌,想测测自己的手气,看看能不能抽到顺子,如果抽到的话,他决定去买体育彩票,嘿嘿！！
# “红心A,黑桃3,小王,大王,方片5”,“Oh My God!”不是顺子.....LL不高兴了,他想了想,决定大\小 王可以看成任何数字,
# 并且A看作1,J为11,Q为12,K为13。上面的5张牌就可以变成“1,2,3,4,5”(大小王分别看作2和4),“So Lucky!”。LL决定去买体育彩票啦。
# 现在,要求你使用这幅牌模拟上面的过程,然后告诉我们LL的运气如何， 如果牌能组成顺子就输出true，否则就输出false。
# 为了方便起见,你可以认为大小王是0。


class Solution:
    def IsContinuous(self, numbers):
        # write code here
        if len(numbers) < 5:
            return False

        # 记录0的个数，并将数列筛分成非0数列
        num_zero = 0
        while 0 in numbers:
            numbers.remove(0)
            num_zero += 1

        # 非0数列只有1个值时，肯定能组成顺子
        if len(numbers) == 1:
            return True

        # 利用集合判断非0数列中是否有重复值，有的话肯定无法组成顺子
        numbers_set = set(numbers)
        if len(numbers) > len(numbers_set):
            return False

        # 非0，且非重复数列中 最大值和最小值的差值小于5时，能够组成顺子
        if max(numbers) - min(numbers) < 5:
            return True
        else:
            return False