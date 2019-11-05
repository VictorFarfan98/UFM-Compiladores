class Node(object):

    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

    def set_next(self, new_next):
        self.next_node = new_next

class IRT(object):
    def __init__(self, head=None):
        self.head = head

    def insert(self, data):
        new_node = Node(data)
        new_node.set_next(self.head)
        self.head = new_node
    
    def iterate(self):
        current = self.head
        while current:
            print(current.data)
            current = current.get_next()

def pseudo_arith_logic(op, var1, var2):
    r = ('{} {} {}').format(op, var1, var2)
    return r

def pseudo_div_mult(op, var1, var2):
    r = ('{} {} {}').format(op, var1, var2)
    return r

def pseudo_shift(op, var1, var2, const):
    r = ('{} {} {} {}').format(op, var1, var2, const)
    return r

def pseudo_shiftV(op, var1, var2, const):
    r = ('{} {} {} {}').format(op, var1, var2, const)
    return r

def pseudo_jump(op, label):
    r = ('{} {}').format(op, label)
    return r

def pseudo_move_from(op, reg):
    r = ('{} {}').format(op, reg)
    return r

def pseudo_branch(branch, var1, var2, label):
    r = ('{} {} {} {}').format(branch, var1, var2, label)
    return r

def pseudo_branch_zero(branch, var1, label):
    r = ('{} {} {}').format(branch, var1, label)
    return r

def pseudo_load_store(op, var1, var2):
    r = ('{} {} {}').format(op, var1, var2)
    return r

'''Head = Node(pseudo_add('var1', 'var2', 'var3'))
inst = IRT(Head)

inst.insert(pseudo_add('d', 'e', 'f'))
'''
print(pseudo_arith_logic('addi', 'a', 'b',))