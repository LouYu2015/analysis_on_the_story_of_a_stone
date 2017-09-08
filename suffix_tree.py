class Node:
    def __init__(self, string, start, end):
        """
        Suffix tree node.

        :param string: whole string
        :param start: index of beginning
        :param end: index of end
        """
        self.string = string
        self.start = start
        self.end = end

        self.next = dict()  # Link to child
        self.counter = None  # Count number of all childs
        self.is_leaf = False  # Is this node a leaf

    def __len__(self):
        return self.end - self.start

    def __str__(self):
        return self.string[self.start: self.end]

    def split(self, i, node):
        """
        Split node at index i.

        :param i: index
        :param node: another child
        :return: splitted node
        """
        new_node = Node(self.string, self.start, self.start + i)
        self.start += i
        new_node.next = {self.string[self.start]: self,
                         self.string[node.start]: node}

        return new_node

    def add_suffix_link(self, destination):
        """
        Add suffex link.
        """
        self.suffix_link = destination
        # destination.reverse_suffix_link.append(self)

    def update_counter(self):
        """
        Update child counter.
        :return: number of children
        """
        if not self.next:
            self.is_leaf = True
            self.counter = 1
        else:
            self.is_leaf = False
            self.counter = sum([child.update_counter() for child in self.next.values()])

        return self.counter

    def visualize(self, current_depth=0):
        """
        Visualize recursively current node and children.

        :param current_depth: current node depth.
        """
        if current_depth == 0:
            print("="*20)

        if len(self) > 10:
            print("\t" * current_depth + "...")
        else:
            print("\t" * current_depth + str(self))

        for child in self.next.values():
            child.visualize(current_depth + 1)


class Cursor:
    def __init__(self, node, branch, length, root=None):
        self.node = node
        self.branch = branch
        self.length = length
        self.root = root

    def current_char(self):
        return str(self.node.next[self.branch])[self.length]

    def move_forward(self, char):
        self.length += 1

        if self.length >= len(self.node.next[self.branch]):
            self.node = self.node.next[self.branch]
            self.branch = char
            self.length -= len(self.node)

    def move_front_forward(self, char):
        assert self.root is not None

        try:
            self.node = self.node.suffix_link
        except AttributeError:
            assert self.length > 0

            self.length -= 1
            self.branch = char
            self.node = self.root

    @property
    def current_node(self):
        return self.node.next[self.branch]

    def print(self):
        self.node.visualize()
        print("Branch: %s, length:%d" % (self.branch, self.length))


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
        update_interval = len(string)//20
        for (i, char) in enumerate(string):
            if i % update_interval == 1:
                print("|", end="", flush=True)

            self.add_char(i, char)
        print()

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

                if prev is not None:
                    prev.add_suffix_link(self.cursor)
                    prev = None
            else:
                if self.length >= len(branch):
                    self.length -= len(branch)
                    self.branch = self.string[i - self.length]
                    self.cursor = branch
                    continue

                if self.string[branch.start + self.length] == char:
                    if prev is not None and self.cursor is not self.root:
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

    def query_cursor(self, string):
        assert string

        cursor = Cursor(self.root, string[0], 0, self.root)
        for char in string[1:]:
            cursor.move_forward(char)
        return cursor

    def query(self, string):
        cursor = self.query_cursor(string)
        return cursor.current_node
