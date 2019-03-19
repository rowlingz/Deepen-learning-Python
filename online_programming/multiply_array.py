# -*- coding:utf-8 -*-
# 题目背景
# 给定一个数组A[0,1,...,n-1],请构建一个数组B[0,1,...,n-1],
# 其中B中的元素B[i]=A[0]*A[1]*...*A[i-1]*A[i+1]*...*A[n-1]。不能使用除法。


def multiply(A):
    # write code here
    # 顺序补充填充
    n = len(A)
    B = [1] * n
    for j in range(1, n):
        B[0] = B[0] * A[j]

    for i in range(1, n - 1):
        for j in range(i):
            B[i] = B[i] * A[j]
        for k in range(i + 1, n):
            B[i] = B[i] * A[k]
    for j in range(n - 1):
        B[n - 1] = B[n - 1] * A[j]
    return B


print(multiply([1, 2, 3, 4, 5]))


def multiply(A):
    # write code here
    length = len(A)
    B = [1] * length

    # 顺序由小填充小于i的值
    for i in range(1, length):
        B[i] = B[i - 1] * A[i - 1]

    # 逆序从大补充大于i的值
    temp = 1
    for i in range(length - 1, -1, -1):
        temp = temp * A[i + 1]
        B[i] = B[i] * temp

    return B