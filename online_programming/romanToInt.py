# -*- coding:utf-8 -*-

# 给定一个罗马数字，将其转换成整数。输入确保在 1 到 3999 的范围内。


class Solution:
    def romanToInt(self, s):
        sign_dicts = {
            'I': 1,
            'IV': 4,
            'V': 5,
            'IX': 9,
            'X': 10,
            'XL': 40,
            'L': 50,
            'XC': 90,
            'C': 100,
            'CD': 400,
            'D': 500,
            'CM': 900,
            'M': 1000
        }
        numbers = 0
        i = 0
        while i < len(s):
            if s[i:i+2] in sign_dicts.keys():
                key = s[i:i+2]
                i += 2
            else:
                key = s[i]
                i += 1
            print(key, '===', sign_dicts[key])
            numbers += sign_dicts[key]

        print(numbers)
        return numbers


if __name__ == '__main__':
    s = Solution()
    # strs = "MCMXCIV"
    # strs = 'LVIII'
    strs = 'IX'
    s.romanToInt(strs)


