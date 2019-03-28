# -*- coding:utf-8 -*-


def insert_sort(lst):
    """插入排序"""
    length = len(lst)
    if length <= 1:
        return lst
    for i in range(1, length):
        for j in range(i):
            if lst[j] > lst[i]:
                lst[i], lst[j] = lst[j], lst[i]

    return lst


def select_sort(lst):
    """直接选择排序"""
    length = len(lst)
    if length <= 1:
        return lst
    for i in range(length-1):
        min_i = i
        for j in range(i+1, length):
            if lst[j] < lst[min_i]:
                min_i = j
        lst[i], lst[min_i] = lst[min_i], lst[i]

    return lst


def bubble_sort(lst):
    """冒泡排序"""
    length = len(lst)
    if length <= 1:
        return lst
    count = 0
    for i in range(length):
        count += 1
        print("第", i, "结果--", lst)
        for j in range(length-i-1):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
    print(count)
    return lst


def bubble_sort2(lst):
    """冒泡排序，添加辅助变量found优化有序序列排序"""
    length = len(lst)
    if length <= 1:
        return lst
    count = 0
    for i in range(length):
        count += 1
        found = False
        for j in range(length-i-1):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
                found = True
        if not found:
            break
    print(count)
    return lst


def bubble_sort3(lst):
    """交错冒泡"""
    length = len(lst)
    if length <= 1:
        return lst
    count = 0
    for i in range(length):
        count += 1
        found = False
        print("第", i, "结果--", lst)
        if i % 2 == 0:
            for j in range(length-i-1):
                if lst[j] > lst[j+1]:
                    lst[j], lst[j+1] = lst[j+1], lst[j]
                    found = True
        else:
            for k in range(length-i-1, i, -1):
                if lst[k] < lst[k-1]:
                    lst[k], lst[k - 1] = lst[k-1], lst[k]
                    found = True
        if not found:
            break
    print(count)
    return lst


def quick_sort(lst):
    def qsort_rec(lst, l, r):
        if l >= r:
            return
        i, j = l, r
        key = lst[i]
        while i < j:
            # 一次划分将序列分成三部分，左序列，key，右序列
            while i < j and lst[j] >= key:
                # 通过j向左扫描找到小于key的值填充在i处
                j -= 1
            if i < j:
                lst[i] = lst[j]
                i += 1
            while i < j and lst[i] <= key:
                # 通过i向右扫描找到大于key的值填充在j处
                i += 1
            if i < j:
                lst[j] = lst[i]
                j -= 1
        lst[i] = key
        # 递归处理左右两个子序列
        qsort_rec(lst, l, i-1)
        qsort_rec(lst, i+1, r)

    qsort_rec(lst, 0, len(lst)-1)
    return lst


def quick_sort1(lst):
    def qsort(lst, left, right):
        if left >= right:
            return
        key = lst[left]
        i = left
        for j in range(left+1, right+1):
            if lst[j] < key:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
        lst[left], lst[i] = lst[i], lst[left]

        qsort(lst, left, i-1)
        qsort(lst, i+1, right)

    qsort(lst, 0, len(lst)-1)
    # return lst


def merge_sort1(lst):
    # 22组合顺序归并

    def merge_pass(lfrom, lto, llen, slen):
        i = 0
        while i + 2 * slen < llen:
            merge(lfrom, lto, i, i + slen, i + 2 * slen)
            i += 2 * slen
        if i + slen < llen:
            merge(lfrom, lto, i, i + slen, llen)
        else:
            for j in range(i, llen):
                lto[j] = lfrom[j]

    def merge(lfrom, lto, low, mid, high):
        i, j, k = low, mid, low
        while i < mid and j < high:
            if lfrom[i] <= lfrom[j]:
                lto[k] = lfrom[i]
                i += 1
            else:
                lto[k] = lfrom[j]
                j += 1
            k += 1
        while i < mid:
            lto[k] = lfrom[i]
            k += 1
            i += 1
        while j < high:
            lto[k] = lfrom[j]
            j += 1
            k += 1

    slen, llen = 1, len(lst)
    templst = [None] * llen
    while slen < llen:
        merge_pass(lst, templst, llen, slen)
        slen *= 2
        merge_pass(templst, lst, llen, slen)
        slen *= 2


def merge_sort(lst):
    # 先拆分再归并
    def merge_1(left, right):
        # 拼接方式1
        result = []
        while left and right:
            if left[0] <= right[0]:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result.extend(left)
        result.extend(right)
        return result

    def merge_(left, right):
        # 拼接方式2：保留列表进行拼接
        i, j = 0, 0
        result = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    if len(lst) <= 1:
        return lst
    mid = len(lst) // 2
    left = lst[:mid]
    right = lst[mid:]

    left_l = merge_sort(left)
    right_l = merge_sort(right)

    return merge_(left_l, right_l)


def bucket_sort_01(lst, n):
    # 适用与0~1之间的小数序列的桶排列
    new_lst = [[] for _ in range(n)]

    for data in lst:
        index = int(data * n)
        new_lst[index].append(data)

    for i in range(n):
        new_lst[i].sort()

    index = 0
    for i in range(n):
        for j in range(len(new_lst[i])):
            lst[index] = new_lst[i][j]
            index += 1
    return lst


def bucket_sort_int(lst):
    # 适用1-M的整数序列的桶排列
    min_n, max_n = min(lst), max(lst)
    new_list = [0] * (max_n - min_n + 1)
    for i in lst:
        new_list[i - min_n] += 1

    index = 0
    current = min_n
    for j in new_list:
        while j > 0:
            lst[index] = current
            j -= 1
            index += 1
        current += 1


if __name__ == '__main__':
    lst = [30, 13, 25, 16, 47, 26, 19, 10]
    # new_lst = insert_sort2(lst)
    # new_lst = select_sort(lst)
    # new_lst = bubble_sort(lst)
    # print(new_lst)
    #
    # lst = [30, 13, 25, 16, 47, 26, 19, 10]
    # new_lst2 = bubble_sort2(lst)
    # print(new_lst2)
    #
    # lst = [30, 13, 25, 16, 47, 26, 19, 10]
    # new_lst3 = bubble_sort3(lst)
    # print(new_lst3)

    # lst = [30, 13, 25, 16, 47, 26, 19, 10]
    # quick_sort1(lst)
    # new_lst = merge_sort(lst)
    # print(lst, new_lst)

    array = [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]
    n = len(array)
    bucket_sort_int(lst)
    print(lst)
