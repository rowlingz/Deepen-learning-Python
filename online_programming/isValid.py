# -*- coding:utf-8 -*-

# 给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串，判断字符串是否有效。
#
# 有效字符串需满足：
#
# 左括号必须用相同类型的右括号闭合。
# 左括号必须以正确的顺序闭合。
# 注意空字符串可被认为是有效字符串。


class Solution:
    def isValid(self, s):
        brackets = {
            '(': ')',
            '{': '}',
            '[': ']'
        }

        if len(s) == 0:
            return True
        elif len(s) == 1:
            return False

        queue_list = []
        for i in s:
            if i in brackets.keys():
                queue_list.append(i)
            elif i in brackets.values():
                if queue_list:
                    if i == brackets[queue_list[-1]]:
                        queue_list.pop()
                    else:
                        return False
                else:
                    return False

        if queue_list:
            return False
        else:
            return True


if __name__ == '__main__':
    s = Solution()
    # strs = "{[]}"
    # strs = ")}{({))[{{[}"
    strs = '(])'
    print(s.isValid(strs))


