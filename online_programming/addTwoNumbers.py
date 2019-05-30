# -*- coding:utf-8 -*-

# 给出两个 非空 的链表用来表示两个非负的整数。其中，它们各自的位数是按照 逆序 的方式存储的，并且它们的每个节点只能存储 一位 数字。
# 如果，我们将这两个数相加起来，则会返回一个新的链表来表示它们的和。
# 您可以假设除了数字 0 之外，这两个数都不会以 0 开头。
#
# 示例：
# 输入：(2 -> 4 -> 3) + (5 -> 6 -> 4)
# 输出：7 -> 0 -> 8
# 原因：342 + 465 = 807


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x, next=None):
        self.val = x
        self.next = next


class Solution:

    def append(self, l, elem):
        p = l
        while p.next is not None:
            p = p.next
        p.next = ListNode(elem)

    def addTwoNumbers(self, l1, l2):
        # 执行用时 : 164 ms, 在Add Two Numbers的Python3提交中击败了29.93% 的用户
        # 内存消耗 : 13 MB, 在Add Two Numbers的Python3提交中击败了97.93% 的用户
        next_val = 0
        result_l = None
        while l1 and l2:
            val = l1.val + l2.val
            next_val += val
            # result_l = ListNode((), result_l)
            if result_l is None:
                result_l = ListNode(next_val % 10)
            else:
                self.append(result_l, (next_val % 10))
            next_val = next_val // 10
            l1 = l1.next
            l2 = l2.next

        while l1:
            next_val += l1.val
            self.append(result_l, (next_val % 10))
            next_val = next_val // 10
            l1 = l1.next
        while l2:
            next_val += l2.val
            self.append(result_l, (next_val % 10))
            next_val = next_val // 10
            l2 = l2.next

        if next_val > 0:
            self.append(result_l, next_val)

        return result_l

    def addTwoNumbers2(self, l1, l2):
        # 执行用时 : 84 ms, 在Add Two Numbers的Python3提交中击败了99.78% 的用户
        # 内存消耗 : 13.1 MB, 在Add Two Numbers的Python3提交中击败了87.70% 的用户
        next_val = 0
        result_l = None
        p = result_l
        while l1 and l2:
            val = l1.val + l2.val
            next_val += val
            # result_l = ListNode((), result_l)
            if result_l is None:
                result_l = ListNode(next_val % 10)
                p = result_l
            else:
                p.next = ListNode(next_val % 10)
                p = p.next
            next_val = next_val // 10
            l1 = l1.next
            l2 = l2.next

        while l1:
            next_val += l1.val
            p.next = ListNode(next_val % 10)
            p = p.next
            next_val = next_val // 10
            l1 = l1.next
        while l2:
            next_val += l2.val
            p.next = ListNode(next_val % 10)
            p = p.next
            next_val = next_val // 10
            l2 = l2.next

        if next_val > 0:
            p.next = ListNode(next_val)

        return result_l


if __name__ == '__main__':
    l1 = ListNode(2, ListNode(4, ListNode(3)))
    # l2 = ListNode(5, ListNode(6, ListNode(4)))
    # l1 = ListNode(0)
    l2 = ListNode(5, ListNode(6, ListNode(7, ListNode(9, ListNode(9)))))
    # l2 = ListNode(0)

    s = Solution()
    result = s.addTwoNumbers2(l1, l2)
    while result:
        print(result.val)
        result = result.next
