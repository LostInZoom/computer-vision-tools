class quad_tree_leaf:
    
    line1=0
    column1=0
    leaf_height=0
    leaf_width=0
    initial_image = None
    parent=None
    childs=[]
    depth = 0

    def __init__(self, line, column, height, width, image, parent):
        self.line1 = line
        self.column1 = column
        self.leaf_height = height
        self.leaf_width = width
        self.initial_image = image
        self.parent = parent
        if (parent != None):
            self.depth = parent.depth + 1

    def addChild(self, child):
        self.childs.append(child)

    def hasChild(self):
        if(len(self.childs)==0):
            return False
        return True

