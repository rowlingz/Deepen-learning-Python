# -*- coding:utf-8 -*-

# 给定两个以字符串形式表示的非负整数 num1 和 num2，返回 num1 和 num2 的乘积，它们的乘积也表示为字符串形式。
# 说明：
#
# num1 和 num2 的长度小于110。
# num1 和 num2 只包含数字 0-9。
# num1 和 num2 均不以零开头，除非是数字 0 本身。
# 不能使用任何标准库的大数类型（比如 BigInteger）或直接将输入转换为整数来处理。


class Solution:
    def multiply(self, num1, num2):
        if 0 in [num1, num2]:
            return '0'
        # num_len1, num_len2 = len(num1), len(num2)
        if len(num1) <= len(num2):
            min_num = num1
            max_num = num2
        else:
            min_num = num2
            max_num = num1

        min_list, max_list = [int(i) for i in min_num], [int(j) for j in max_num]
        min_len, max_len = len(min_num), len(max_num)

        cols = min_len + max_len - 1
        rows = sum(min_list)

        results = []
        for i in range(min_len):
            current_list = [0] * cols
            if i == 0:
                current_list[-max_len:] = max_list
            else:
                current_list[-max_len - i:-i] = max_list

            j = min_list[-i-1]

            while j > 0:
                results.append(current_list)
                j -= 1

        print(results)
        # df = pd.DataFrame(results)
        # print(df)

        data_sum = []
        previous = 0
        for col in range(cols-1, -1, -1):
            # current_sum = sum(df[col]) + previous
            current_sum = sum(results[row][col] for row in range(rows)) + previous
            current_num = current_sum % 10
            previous = current_sum // 10
            data_sum.insert(0, current_num)
        if previous:
            data_sum.insert(0, previous)

        print(''.join(str(i) for i in data_sum))

        return ''.join(str(i) for i in data_sum)


if __name__ == '__main__':
    s = Solution()
    num1 = '2'
    num2 = '3'
    s.multiply(num1, num2)
