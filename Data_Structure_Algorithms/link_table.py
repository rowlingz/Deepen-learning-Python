# -*- coding:utf-8 -*-


class LNode:
    """单链表结点类"""
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next_ = next_


class LList:
    """简单单链表类"""
    def __init__(self):
        # 下划线开头用作内部对象
        self._head = None

    def is_empty(self):
        return self._head is None

    def prepend(self, elem):
        # 表头插入元素
        self._head = LNode(elem, self._head)

    def pop(self):
        if self._head is None:
            raise Exception
        e = self._head.elem
        self._head = self._head.next_
        return e

    def append(self, elem):
        if self._head is None:
            self._head = LNode(elem)
            return
        p = self._head
        while p.next_ is not None:
            p = p.next_
        p.next_ = LNode(elem)

    def pop_last(self):
        if self._head is None:
            raise Exception

        p = self._head
        if p.next_ is None:
            e = p.elem
            self._head = None
            return e

        while p.next_.next_ is not None:
            p = p.next_

        e = p.next_.elem
        p.next_ = None
        return e

    def filter(self, pred):
        p = self._head
        while p is not None:
            if pred(p.elem):
                yield p.elem
            p = p.next_

    def printall(self):
        p = self._head
        while p is not None:
            print(p.elem, end=" ")
            if p.next_ is not None:
                print(", ", end=' ')
            p = p.next_
        print(" ")

    def elements(self):
        p = self._head
        while p is not None:
            yield p.elem
            p = p.next_

    def rev(self):
        p = None
        while self._head is not None:
            q = self._head
            self._head = q.next_
            q.next_ = p
            p = q
        self._head = p
        print()

    def sort1(self):
        # 通过移动元素进行排序
        if self._head is None:
            return
        crt = self._head.next_
        while crt is not None:
            x = crt.elem        # 查到需要排序的元素
            p = self._head      # 在已排序中从头查找需要交换的位置
            while p is not crt and p.elem <= x:    # 排除小元素
                p = p.next_
            while p is not crt:     # 利用元素交换完成元素插入及后移
                y = p.elem
                p.elem = x
                x = y
                p = p.next_
            crt.elem = x
            crt = crt.next_

    def sort(self):
        p = self._head
        if p is None or p.next_ is None:
            return

        rem = p.next_
        p.next_ = None
        while rem is not None:
            p = self._head
            q = None
            while p is not None and p.elem <= rem.elem:
                q = p
                p = p.next_
            if q is None:
                self._head = rem
            else:
                q.next_ = rem
            q = rem
            rem = rem.next_
            q.next_ = p


class LList1(LList):
    """含尾节点的单链表"""
    def __init__(self):
        LList.__init__(self)
        self._rear = None

    def prepend(self, elem):
        if self._head is None:
            self._head = LNode(elem, self._head)
            self._rear = self._head
        else:
            self._head = LNode(elem, self._head)

    def append(self, elem):
        if self._head is None:
            self._head = LNode(elem, self._head)
            self._rear = self._head
        else:
            self._rear.next_ = LNode(elem)
            self._rear = self._rear.next_

    def pop_last(self):
        if self._rear is None:
            raise Exception
        p = self._head
        if p.next_ is None:
            e = p.elem
            self._head =None
            return e
        while p.next_.next_ is not None:
            p = p.next_
        e = p.next_.elem
        p.next_ = None
        self._rear = p
        return e


class LCList:
    """循环单链表"""
    def __init__(self):
        self._rear = None

    def is_empty(self):
        return self._rear is None

    def prepend(self, elem):
        p = LNode(elem)
        if self._rear is None:
            p.next_ = p
            self._rear = p
        else:
            p.next_ = self._rear.next_
            self._rear.next_ = p

    def append(self, elem):
        self.prepend(elem)
        self._rear = self._rear.next_

    def pop(self):
        if self._rear is None:
            raise Exception
        p = self._rear.next_
        if self._rear is p:
            self._rear = None
        else:
            self._rear.next_ = p.next_
        return p.elem

    def printall(self):
        if self.is_empty():
            return
        p = self._rear.next_
        while True:
            yield p.elem
            if p is self._rear:
                break
            p = p.next_


class DLNode(LNode):
    def __init__(self, elem, prev=None, next_=None):
        LNode.__init__(self, elem, next_)
        self.pre = prev


class DLList(LList1):
    def __init__(self):
        LList1.__init__(self)

    def prepend(self, elem):
        p = DLNode(elem, None, self._head)
        if self._head is None:
            self._rear = p
        else:
            p.next_.prev = p
        self._head = p

    def append(self, elem):
        p = DLNode(elem, self._rear, None)
        if self._head is None:
            self._head = p
        else:
            p.prev.next_ = p
        self._rear = p

    def pop(self):
        if self._head is None:
            raise Exception
        e = self._head.elem
        self._head = self._head.next_
        if self._head is None:
            self._head.prev = None
        return e

    def pop_last(self):
        if self._head is None:
            raise Exception
        e = self._rear.elem
        self._rear = self._rear.prev
        if self._rear is None:
            self._head = None
        else:
            self._rear.next_ = None
        return e


class Josephus(LCList):
    """循环单链表 解决Josephus"""
    def turn(self, m):
        for i in range(m):
            self._rear = self._rear.next_

    def __init__(self, n, k, m):
        LCList.__init__(self)
        for i in range(n):
            self.append(i+1)

        self.turn(k-1)

        while not self.is_empty():
            self.turn(m-1)
            print(self.pop(), end="\n" if self.is_empty() else ", ")

# elem_list = [4, 2,3,1,6,7]
# mlist1 = LList()

# for i in elem_list:
    # print(i)
    # mlist1.append(i)
    # print([i for i in mlist1.elements()])

# mlist1.printall()
# print([i for i in mlist1.elements()])
# print([i for i in mlist1.filter(lambda x: x % 2 == 0)])
# mlist1.sort()
# print([i for i in mlist1.elements()])

Josephus(5, 3, 2)