from Node import Node
import judge as j

'''j.main()'''


p = Node(data=1)
f = Node(data=2)

p.add_child(f)

print(f.get_parent().get_data())