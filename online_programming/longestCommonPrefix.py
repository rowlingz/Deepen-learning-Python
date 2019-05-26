# -*- coding:utf-8 -*-

# 编写一个函数来查找字符串数组中的最长公共前缀。如果不存在公共前缀，返回空字符串 ""。


class Solution:
    def longestCommonPrefix(self, strs):
        if len(strs) == 0:
            return ''
        str_lens = [len(s) for s in strs]
        min_lens = min(str_lens)
        min_str = strs[0]
        common_prefix = []
        i = 0
        while i < min_lens:
            strs_i = [s[i] for s in strs]
            if len(set(strs_i)) == 1:
                common_prefix.append(min_str[i])
                i += 1
            else:
                break
        return ''.join(common_prefix)


if __name__ == '__main__':
    s = Solution()
    # strs = ["flower","flow","flight"]
    strs = ["dog", "racecar", "car"]
    print(s.longestCommonPrefix(strs))


