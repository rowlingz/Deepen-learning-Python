# -*- coding:utf-8 -*-
# 在数组中的两个数字，如果前面一个数字大于后面的数字，则这两个数字组成一个逆序对。
# 输入一个数组,求出这个数组中的逆序对的总数P。并将P对1000000007取模的结果输出。 即输出P%1000000007
import time
import numpy as np


def InversePairs(data):
    """归并方式求解"""
    global count

    def merge_sort(data):
        global count
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left_l = data[:mid]
        right_l = data[mid:]
        left = merge_sort(left_l)
        right = merge_sort(right_l)
        # merge(left_l, right_l)

        result = []
        r = len(right)
        while left and right:
            if left[0] < right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
                count += len(left)

        if left:
            result.extend(left)
            # count += (len(left) - 1) * r
        result.extend(right)

        return result

    count = 0
    merge_sort(data)
    return count % 1000000007


def reverse(data):
    """暴力求解"""
    length = len(data)
    count = 0
    for i in range(length-1):
        for j in range(i+1, length):
            if data[i] > data[j]:
                count += 1

    return count % 1000000007


if __name__ == "__main__":
    data = list(np.random.permutation(range(1000)))
    t1 = time.clock()
    print(InversePairs(data))
    t2 = time.clock()
    print("归并排序运行时间", t2-t1)

    print(reverse(data))
    t3 = time.clock()
    print(t3)
    print("直接排序时间： ", t3-t2)


