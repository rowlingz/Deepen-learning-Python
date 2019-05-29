# -*- coding:utf-8 -*-

# 给定一个整数，将其转为罗马数字。输入确保在 1 到 3999 的范围内。


class Solution:
    def intToRoman(self, num):
        roman_sign = [['I', 'V'], ['X', 'L'], ['C', 'D'], ['M', '']]
        result = []
        i = 0
        while num > 0:
            current = num % 10
            if current <= 3:
                result.insert(0, roman_sign[i][0] * current)
            elif current == 4:
                result.insert(0, roman_sign[i][0] + roman_sign[i][1])
            elif current <= 8:
                result.insert(0, roman_sign[i][1] + roman_sign[i][0] * (current % 5))
            elif current == 9:
                result.insert(0, roman_sign[i][0] + roman_sign[i+1][0])

            i += 1
            num = num // 10

        return ''.join(result)


if __name__ == '__main__':
    s = Solution()
    num = 1
    # num = 3999

    s.intToRoman(num)





