class Node:
    def __init__(self, string, start, end):
        self.string = string
        self.start = start
        self.end = end

        self.next = dict()
        self.reverse_suffix_link = list()
        self.counter = None
        self.is_leaf = False

    def split(self, i, node):
        new_node = Node(self.string, self.start, self.start + i)
        self.start += i

        new_node.next = {self.string[self.start]: self,
            self.string[node.start]: node}

        return new_node

    def add_suffix_link(self, to_node):
        self.suffix_link = to_node
        to_node.reverse_suffix_link.append(self)

    def __len__(self):
        return self.end - self.start

    def __str__(self):
        return self.string[self.start: self.end]

    def str_with_split(self):
        if place_holder in str(self):
            return str(self)[:str(self).index(place_holder)]
        else:
            return str(self)

    def update_counter(self):
        if not self.next:
            self.is_leaf = True
        else:
            self.is_leaf = False

        if self.is_leaf:
            self.counter = 1
        else:
            self.counter = 0
            for child in self.next.values():
                self.counter += child.update_counter()

        return self.counter

    def visualize(self, index=0):
        print('\t'*index + str(self))
        for child in self.next.values():
            child.visualize(index + 1)


class Cursor:
    def __init__(self, node, branch, length):
        self.node = node
        self.branch = branch
        self.length = length

    def current_char(self):
        return str(self.node.next[self.branch])[self.length]

    def move_forward(self, char):
        self.length += 1

        if self.length >= len(self.node):
            self.branch = char
            self.node = self.node.next[self.branch]
            self.length = 0

    def move_front_forward(self):
        pass

class SuffixTree:
    def __init__(self, string):
        self.string = string
        self.root = Node(string, 0, 0)

        self.cursor = self.root
        self.branch = string[0]
        self.length = 0
        self.remaining = 0

        self.construct(string)

    def construct(self, string):
        for (i, char) in enumerate(string):
            self.add_char(i, char)

    def add_char(self, i, char):
        self.remaining += 1
        prev = None

        while self.remaining > 0:
            if self.length == 0:
                self.branch = char

            try:
                branch = self.cursor.next[self.branch]
            except KeyError:
                branch = self.cursor.next[self.branch] = Node(self.string, i, len(self.string))

                if prev != None:
                    prev.add_suffix_link(self.cursor)
                    prev = None
            else:
                if self.length >= len(branch):
                    self.length -= len(branch)
                    self.branch = self.string[i - self.length]
                    self.cursor = branch
                    continue

                if self.string[branch.start + self.length] == char:
                    if prev != None and self.cursor is not self.root:
                        prev.add_suffix_link(self.cursor)
                    self.length += 1
                    return

                new_node = Node(self.string, i, len(self.string))
                branch = self.cursor.next[self.branch] = branch.split(self.length, new_node)

                if prev:
                    prev.add_suffix_link(branch)
                prev = branch

            self.remaining -= 1
            if self.cursor is self.root:
                if self.length > 0:
                    self.length -= 1
                    self.branch = self.string[i - self.remaining + 1]
            else:
                try:
                    self.cursor = self.cursor.suffix_link
                except AttributeError:
                    self.cursor = self.root

    def update_counter(self):
        self.root.update_counter()

    def query(self, string):
        assert string

        cursor = Cursor(self.root, string[0], 0)
        for char in string:
            cursor.move_forward(char)
        return cursor.node
