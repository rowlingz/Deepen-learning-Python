# -*- coding:utf-8 -*-
# 给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if len(s) == 0:
            return 0
        length = 1
        max_length = 1
        sub_string = [s[0]]
        for i in range(1, len(s)):
            if s[i] in sub_string:
                sub_index = sub_string.index(s[i])
                if length > max_length:
                    max_length = length
                sub_string = sub_string[sub_index+1:]
                sub_string.append(s[i])
                length = length - sub_index
            else:
                length += 1
                sub_string.append(s[i])
        if length > max_length:
            max_length = length
        return max_length


if __name__ == '__main__':

    # string = "aabaab!bb"
    string = 'abcabcb'
    s = Solution()
    print(s.lengthOfLongestSubstring(string))
