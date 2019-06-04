# -*- coding:utf-8 -*-

# 给定一个排序数组，你需要在原地删除重复出现的元素，使得每个元素只出现一次，返回移除后数组的新长度。
# 不要使用额外的数组空间，你必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成。


class Solution:
    def removeDuplicates(self, nums):
        # 给定一个排序数组，你需要在原地删除重复出现的元素，使得每个元素只出现一次，返回移除后数组的新长度。
        # 不要使用额外的数组空间，你必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成。

        # 执行用时 : 76 ms, 在Remove Duplicates from Sorted Array的Python3提交中击败了94.17% 的用户
        # 内存消耗 : 14.6 MB, 在Remove Duplicates from Sorted Array的Python3提交中击败了93.52% 的用户
        if len(nums) <= 1:
            return len(nums)
        length = len(nums)
        max_id, next_id = 0, 0
        while next_id <= length-1:
            while next_id <= length-2 and nums[next_id] == nums[next_id+1]:
                next_id += 1

            nums[max_id] = nums[next_id]
            max_id += 1
            next_id += 1
        return max_id

    def removeDuplicatesTwo(self, nums):
        # 给定一个排序数组，你需要在原地删除重复出现的元素，使得每个元素最多出现两次，返回移除后数组的新长度。
        # 不要使用额外的数组空间，你必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成。

        # 执行用时 : 60 ms, 在Remove Duplicates from Sorted Array II的Python3提交中击败了95.83% 的用户
        # 内存消耗 : 12.8 MB, 在Remove Duplicates from Sorted Array II的Python3提交中击败了99.20% 的用户

        length = len(nums)
        if length <= 2:
            return length

        max_id, next_id = 0, 0
        while next_id <= length-2:
            while next_id <= length-3 and nums[next_id] == nums[next_id+1] and nums[next_id] == nums[next_id+2]:
                next_id += 1
            if nums[next_id] == nums[next_id+1]:
                nums[max_id] = nums[next_id]
                nums[max_id+1] = nums[next_id]
                max_id += 2
                next_id += 2
            else:
                nums[max_id] = nums[next_id]
                max_id += 1
                next_id += 1
        if next_id < length:
            nums[max_id] = nums[next_id]
            max_id += 1
        print(nums[:max_id])
        return max_id

    def removeElement(self, nums, val):
        # 给定一个数组 nums 和一个值 val，你需要原地移除所有数值等于 val 的元素，返回移除后数组的新长度。
        # 不要使用额外的数组空间，你必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成。
        # 元素的顺序可以改变。你不需要考虑数组中超出新长度后面的元素。

        # 执行用时 : 44 ms, 在Remove Element的Python3提交中击败了98.23% 的用户
        # 内存消耗 : 13.1 MB, 在Remove Element的Python3提交中击败了77.74% 的用户
        length = len(nums)
        end_id, next_id = 0, 0
        while next_id <= length-1:
            if nums[next_id] == val:
                next_id += 1
            else:
                nums[end_id] = nums[next_id]
                end_id += 1
                next_id += 1
        print(nums)
        return end_id


if __name__ == '__main__':
    s = Solution()
    # nums = [0,0,1,1,1,2,2,3,3,4]
    # nums = [1,1]
    # nums = [0,0,0,0]
    # nums = [1, 1, 2]
    # nums = [1,1,1,2,2,3]
    # result = s.removeDuplicatesTwo(nums)
    # result = s.removeDuplicates2(nums)

    # nums = [3, 2, 2, 3]
    nums = [0,1,2,2,3,0,4,2]
    val = 2
    result = s.removeElement(nums, val)
    print(result)
