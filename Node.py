# Node class
class Node(object):
    def __init__(self, data=None):
        self.data = data
        self.children = []
        self.parent = None
        self.next_hop = []

    def add_child(self, obj):
        for o in obj:
            o.set_parent(self)
            self.children.append(o)

    def set_parent(self, parent):
        self.parent = parent

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children

    def set_next_hop(self, next_hop):
        self.next_hop = next_hop

    def get_next_hop(self):
        return self.next_hop

    def print_node(self):
        print('{0}\n'.format(self.data))
        for child in self.children:
            print('\t{0}'.format(child.print_node()))
