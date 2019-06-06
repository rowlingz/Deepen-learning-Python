# -*- coding:utf-8 -*-
class ListNode:
    def __init__(self, x, next=None):
        self.val = x
        self.next = next


class MyLinkedList(object):

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.head = None

    def get(self, index):
        """
        Get the value of the index-th node in the linked list. If the index is invalid, return -1.
        :type index: int
        :rtype: int
        """
        if self.head is None:
            return -1
        else:
            if index < 0:
                return -1
            i = 0
            p = self.head
            while p:
                if i == index:
                    return p.val
                else:
                    p = p.next
                    i += 1
            if i <= index:
                return -1

    def addAtHead(self, val):
        """
        Add a node of value val before the first element of the linked list. After the insertion, the new node will be the first node of the linked list.
        :type val: int
        :rtype: None
        """
        if self.head is None:
            self.head = ListNode(val)
        else:
            p = ListNode(val)
            p.next = self.head
            self.head = p

    def addAtTail(self, val):
        """
        Append a node of value val to the last element of the linked list.
        :type val: int
        :rtype: None
        """
        if self.head is None:
            self.head = ListNode(val)
        else:
            p = self.head
            while p.next:
                p = p.next
            p.next = ListNode(val)

    def addAtIndex(self, index, val):
        """
        Add a node of value val before the index-th node in the linked list. If index equals to the length of linked list, the node will be appended to the end of linked list. If index is greater than the length, the node will not be inserted.
        :type index: int
        :type val: int
        :rtype: None
        """
        if self.head is None:
            if index <= 0:
                self.head = ListNode(val)
            return
        else:
            if index <= 0:
                self.addAtHead(val)
            else:
                i = 1
                p = self.head
                while p.next:
                    if i == index:
                        q = p.next
                        p.next = ListNode(val)
                        p = p.next
                        p.next = q
                        return
                    else:
                        p = p.next
                        i += 1
                if i == index:
                    p.next = ListNode(val)

    def deleteAtIndex(self, index):
        """
        Delete the index-th node in the linked list, if the index is valid.
        :type index: int
        :rtype: None
        """
        if self.head:
            if index < 0:
                return
            elif index == 0:
                self.head = self.head.next
            else:
                i = 1
                p = self.head
                while p.next:
                    if i == index:
                        if p.next.next:
                            p.next = p.next.next
                        else:
                            p.next = None
                        return
                    else:
                        p = p.next
                        i += 1


obj = MyLinkedList()
# obj.addAtHead(1)
# obj.addAtTail(3)
obj.addAtIndex(-1, 0)
obj.get(0)
obj.deleteAtIndex(-1)
# obj.get(-3)
