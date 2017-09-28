from Node import Node
import operator

root = Node()
#
# level_1_1 = Node()
# level_1_2 = Node()
#
# level_2_1 = Node()
# level_2_2 = Node()
# level_2_3 = Node()
# level_2_4 = Node()
#
# level_3_1 = Node()
# level_3_2 = Node()
# level_3_3 = Node()
# level_3_4 = Node()
# level_3_5 = Node()
# level_3_6 = Node()
# level_3_7 = Node()
# level_3_8 = Node()
#
# level_4_1 = Node(data=8)
# level_4_2 = Node(data=7)
# level_4_3 = Node(data=3)
# level_4_4 = Node(data=9)
# level_4_5 = Node(data=9)
# level_4_6 = Node(data=8)
# level_4_7 = Node(data=2)
# level_4_8 = Node(data=4)
# level_4_9 = Node(data=1)
# level_4_10 = Node(data=8)
# level_4_11 = Node(data=8)
# level_4_12 = Node(data=9)
# level_4_13 = Node(data=9)
# level_4_14 = Node(data=9)
# level_4_15 = Node(data=3)
# level_4_16 = Node(data=4)
#
# root.add_child([level_1_1,level_1_2])
#
# level_1_1.add_child([level_2_1,level_2_2])
# level_1_2.add_child([level_2_3,level_2_4])
#
# level_2_1.add_child([level_3_1,level_3_2])
# level_2_2.add_child([level_3_3,level_3_4])
# level_2_3.add_child([level_3_5,level_3_6])
# level_2_4.add_child([level_3_7,level_3_8])
#
# level_3_1.add_child([level_4_1,level_4_2])
# level_3_2.add_child([level_4_3,level_4_4])
# level_3_3.add_child([level_4_5,level_4_6])
# level_3_4.add_child([level_4_7,level_4_8])
# level_3_5.add_child([level_4_9,level_4_10])
# level_3_6.add_child([level_4_11,level_4_12])
# level_3_7.add_child([level_4_13,level_4_14])
# level_3_8.add_child([level_4_15,level_4_16])

def getMiniMax(root,isMax=True):
    data = root.get_data()
    if not data:
        childrenData = []
        childrenHop = []

        for child in root.get_children():
            childrenData.append(getMiniMax(child, not isMax))
            childrenHop.append(child.get_next_hop())

        if isMax:
            index, data = max(enumerate(childrenData), key=operator.itemgetter(1))
        else:
            index, data = min(enumerate(childrenData), key=operator.itemgetter(1))

        next_hop = childrenHop[index]
        next_hop.insert(0, index)
        root.set_next_hop(next_hop)
        root.set_data(data)

    return data

def make_best_move(board, turn):
    


getMiniMax(root)

print(root.get_next_hop()[0])
# print(root.get_data())
