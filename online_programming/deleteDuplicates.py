# -*- coding:utf-8 -*-


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x, next=None):
        self.val = x
        self.next = next


class Solution:
    def deleteDuplicates(self, head):
        # 给定一个排序链表，删除所有重复的元素，使得每个元素只出现一次。
        if not head:
            return None
        p = head
        while p.next:
            q = p.next
            if p.val == q.val:
                p.next = p.next.next
            else:
                p = p.next
        return head

    def deleteDuplicatesTwo(self, head):
        # 给定一个排序链表，删除所有含有重复数字的节点，只保留原始链表中 没有重复出现 的数字。
        new = ListNode(0)
        p = new

        while head:
            if head.next and head.val == head.next.val:
                # 记录重复的值，删除重复的节点后，新的链表指向下一个不重复的节点
                dup_val = head.val
                while head and head.val == dup_val:
                    head = head.next
                p.next = head
            else:
                # 不存在重复值，按节点依次移动
                p.next = head
                p = head
                head = head.next
        return new.next

    def mergeTwoLists(self, l1, l2):
        # 将两个有序链表合并为一个新的有序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。
        p = ListNode(0)
        new = p
        while l1 and l2:
            if l1.val < l2.val:
                p.next = l1
                l1 = l1.next
            else:
                p.next = l2
                l2 = l2.next

        if l1:
            p.next = l1

        if l2:
            p.next = l2

        return new.next

    def removeElements(self, head, val):
        # 删除链表中等于给定值 val 的所有节点。

        # 执行用时 : 96 ms, 在Remove Linked List Elements的Python3提交中击败了93.09% 的用户
        # 内存消耗 : 16.2 MB, 在Remove Linked List Elements的Python3提交中击败了96.38% 的用户
        if not head:
            return None
        p = ListNode(0)
        p.next = head
        new = p
        while head.next:
            if head.val == val:
                head = head.next
            else:
                p.next = head
                p = p.next
                head = head.next
        if head.next is None:
            if head.val == val:
                p.next = None
            else:
                p.next = head
        return new.next


if __name__ == '__main__':
    l1 = ListNode(1, ListNode(7, ListNode(8)))
    # l2 = ListNode(5, ListNode(6, ListNode(4)))
    # l1 = ListNode(0)
    l2 = ListNode(6, ListNode(7, ListNode(7, ListNode(7, ListNode(7, ListNode(11, ListNode(20)))))))
    # l2 = ListNode(0)

    # head = ListNode(1, ListNode(2, ListNode(6, ListNode(3, ListNode(4, ListNode(5, ListNode(6)))))))
    head = ListNode(1, ListNode(2))

    s = Solution()
    # result = s.deleteDuplicatesTwo(l1)
    # result = s.mergeTwoLists(l1, l2)
    result = s.removeElements(head, 1)
    while result:
        print(result.val)
        result = result.next

