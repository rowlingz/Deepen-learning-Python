# -*- coding:utf-8 -*-

# 将一个给定字符串根据给定的行数，以从上往下、从左到右进行 Z 字形排列。
# 之后，你的输出需要从左往右逐行读取，产生出一个新的字符串，


class Solution:
    def convert(self, s, numRows):
        # 执行用时 : 100 ms, 在ZigZag Conversion的Python3提交中击败了78.79% 的用户
        # 内存消耗 : 13.1 MB, 在ZigZag Conversion的Python3提交中击败了95.19% 的用户

        if numRows == 1:
            return s
        i, j = 0, 0
        result = [[]]
        while j < numRows-1:
            result.append([])
            j += 1

        k = 0
        # if k < len(s):
        while k < len(s):
            while k < len(s) and i < numRows:
                result[i].append(s[k])
                i += 1
                k += 1
            i -= 1
            while k < len(s) and i > 0:
                i -= 1
                result[i].append(s[k])
                k += 1
            i += 1
        print(result)
        return ''.join(''.join(col) for col in result)


if __name__ == '__main__':
    s = Solution()
    # strs = "LEETCODEISHIRING"
    # numRows = 4

    strs = "AB"
    numRows = 1
    result = s.convert(strs, numRows)
    print(result)









