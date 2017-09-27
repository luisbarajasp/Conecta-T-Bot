# Node class
class Node(object):
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
    
    def add_child(self, obj):
        obj.set_parent(self)
        self.children.append(obj)
    
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