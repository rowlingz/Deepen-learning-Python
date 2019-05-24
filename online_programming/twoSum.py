# -*- coding:utf-8 -*-
# 给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
# 你可以假设每种输入只会对应一个答案。但是，你不能重复利用这个数组中同样的元素。


class Solution:
    def twoSum(self, nums, target):
        length = len(nums)
        if length == 0:
            return None
        elif length == 1:
            if nums[0] == target:
                return [0]
            else:
                return None

        for i in range(length - 1):
            first_num = nums[i]
            diff = target - first_num
            if diff in nums[i + 1:]:
                diff_sub = nums[i + 1:].index(diff)
                return [i, i+1+diff_sub]
        return None


if __name__ == '__main__':
    nums = [2, 7, 11, 15]
    target = 9

    s = Solution()

    print(s.twoSum(nums, target))

