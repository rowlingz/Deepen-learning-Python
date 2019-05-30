# -*- coding:utf-8 -*-

# 给定两个大小为 m 和 n 的有序数组 nums1 和 nums2。
# 请你找出这两个有序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))。
# 你可以假设 nums1 和 nums2 不会同时为空。


class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        # 执行用时 : 132 ms, 在Median of Two Sorted Arrays的Python3提交中击败了34.24% 的用户
        # 内存消耗 : 13 MB, 在Median of Two Sorted Arrays的Python3提交中击败了99.33% 的用户

        length1, length2 = len(nums1), len(nums2)
        mid = (length1 + length2) // 2
        print(mid)

        i = 0
        result = []
        i_1, i_2 = 0, 0
        while i_1 < length1 and i_2 < length2:
            if i < mid + 1:
                if nums1[i_1] < nums2[i_2]:
                    result.append(nums1[i_1])
                    i += 1
                    i_1 += 1
                elif nums1[i_1] > nums2[i_2]:
                    result.append(nums2[i_2])
                    i += 1
                    i_2 += 1
                elif nums1[i_1] == nums2[i_2]:
                    result.append(nums1[i_1])
                    result.append(nums2[i_2])
                    i += 2
                    i_1 += 1
                    i_2 += 1
            else:
                break

        while i < mid + 1:
            i += 1
            if i_1 < length1:
                result.append(nums1[i_1])
                i_1 += 1
            if i_2 < length2:
                result.append(num2[i_2])
                i_2 += 1

        print(result)
        if (length1 + length2) % 2 == 1:
            return result[mid]
        else:
            return (result[mid] + result[mid-1]) / 2


if __name__ == '__main__':
    s = Solution()
    num1 = [1]
    num2 = [3]
    # num1 = [1, 3]
    # num2 = [2]

    mid_num = s.findMedianSortedArrays(num1, num2)
    print(mid_num)


