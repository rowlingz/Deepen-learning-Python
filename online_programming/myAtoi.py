# -*- coding:utf-8 -*-

# 实现一个 atoi 函数，使其能将字符串转换成整数。
# 首先，该函数会根据需要丢弃无用的开头空格字符，直到寻找到第一个非空格的字符为止。
# 当我们寻找到的第一个非空字符为正或者负号时，则将该符号与之后面尽可能多的连续数字组合起来，作为该整数的正负号；
# 假如第一个非空字符是数字，则直接将其与之后连续的数字字符组合起来，形成整数。
# 该字符串除了有效的整数部分之后也可能会存在多余的字符，这些字符可以被忽略，它们对于函数不应该造成影响。
# 注意：假如该字符串中的第一个非空格字符不是一个有效整数字符、字符串为空或字符串仅包含空白字符时，则你的函数不需要进行转换。
# 在任何情况下，若函数不能进行有效的转换时，请返回 0。


class Solution:
    def myAtoi(self, strs):
        strs = strs.lstrip()
        if len(strs) == 0:
            return 0
        first_str = strs[0]
        if first_str == '-':
            strs = strs[1:]
            mark = '-'
        elif first_str == '+':
            strs = strs[1:]
            mark = '+'
        else:
            mark = '+'
        result = ['0']
        for i in range(len(strs)):
            try:
                current_num = int(strs[i])
                result.append(str(current_num))
            except ValueError:
                break

        numbers = mark + ''.join(result)
        numbers = int(numbers)
        if numbers >= 2147483648:
            return 2147483648
        elif numbers > -2147483648:
            return numbers
        else:
            return -2147483648


if __name__ == '__main__':
    s = Solution()
    # strs = '-91283472332'
    strs = '+1'
    print(s.myAtoi(strs))

