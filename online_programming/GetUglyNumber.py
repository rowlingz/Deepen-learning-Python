# -*- coding:utf-8 -*-
# 把只包含质因子2、3和5的数称作丑数（Ugly Number）。例如6、8都是丑数，但14不是，因为它包含质因子7。
# 习惯上我们把1当做是第一个丑数。求按从小到大的顺序的第N个丑数。
import time


def GetUglyNumber_Solution(index):

    """除1外，丑数主要来源于现有丑数的2， 3， 5倍，"""

    if index <= 0:
        return 0
    if index == 1:
        return 1
    ugly_lists = [1]

    # 为2，3，5创建倍数索引，
    i_2, i_3, i_5 = 0, 0, 0
    for i in range(1, index):

        # 下一个丑数来源于未加入的2， 3，5倍数值的最小值
        new_ugly = min([ugly_lists[i_2] * 2, ugly_lists[i_3] * 3, ugly_lists[i_5] * 5])
        ugly_lists.append(new_ugly)

        # 找到最小值来源于2， 3， 5中的哪个倍数值，对应索引值＋1，
        # 这里要注意2*3，3*2这类存在相同的值，因此需要逐一验证，不可直接跳出循环。
        if ugly_lists[i] == ugly_lists[i_2] * 2:
            i_2 += 1
        if ugly_lists[i] == ugly_lists[i_3] * 3:
            i_3 += 1
        if ugly_lists[i] == ugly_lists[i_5] * 5:
            i_5 += 1

    return ugly_lists[-1]


if __name__ == '__main__':

    for i in range(10):
        print(GetUglyNumber_Solution(i))

    t = time.clock()
    print(GetUglyNumber_Solution(1000))
    print("运行时间：", time.clock())