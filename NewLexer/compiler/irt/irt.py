#from ast import eval
import sys, os
sys.path.insert(0, '../parser/')
import anytree
from anytree import Node, RenderTree, PostOrderIter, PreOrderIter, LevelOrderIter
import Parser


registros = {}
RAM = {}
mem_pos = -4

class Nodos(object):

    def __init__(self, data=None, next_node=None, next_if=None):
        self.data = data
        self.next_node = next_node
        self.next_if = next_if

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node
    
    def get_next_if(self):
        return self.next_if

    def set_next(self, new_next):
        self.next_node = new_next

class IRT(object):
    def __init__(self, head=None):
        self.head = head

    def insert(self, data):
        new_node = Nodos(data)
        new_node.set_next(self.head)
        self.head = new_node
    
    def iterate(self):
        current = self.head
        
        if os.path.exists("../code_gen/IRT.txt"):
            os.remove("../code_gen/IRT.txt")
        while current:
            with open('../code_gen/IRT.txt', 'a+') as f:
                f.write(current.data+'\n')
            print(current.data)
            #print('   ↓    ')
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

def pseudo_create_label(op, label):
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

def getExprValue(exprNode, expectedType = None):
        operation = ""
        operators = ['+','-','*','%',"(",")"]
        for node in PostOrderIter(exprNode):
            #print(type(node.name) == list)
            if type(node.name) == list:                                
                if node.name[0] == "ID":
                    if self.LookupType(node.name[1]) != expectedType:
                        raise Exception("Invalid type found for", expectedType, "operation")
                    if node.parent.name == "method_call":
                        #Implementar metodo para recuperar el valor de una method call
                        pass
                    else:
                        operation += str(self.Lookup(node.name[1])[1])
                    #operation += super(SemanticRules, self).Lookup(node.name[1])[1]
                else:
                    #print(node.name)
                    if expectedType == "int":
                        if node.name[1].isnumeric() or node.name[1] in operators:
                            operation += node.name[1]
                        else:
                            raise Exception("Invalid type found for <", expectedType, "> operation")
                    elif expectedType == "boolean":
                        if not node.name[1].isnumeric():
                            operation += node.name[1]
                        else:
                            raise Exception("Invalid type found for <", expectedType, "> operation")
        return operation

Head = None
inst = IRT(Head)
leftsibling = anytree.util.leftsibling
rightsibling = anytree.util.rightsibling
tf = []
instructions = []
for_labels = []
for_label_counter = 0
else_labels = []
strings = []
else_label_counter = 0
block_index = None
post = [node for node in PostOrderIter(Parser.g.final_tree)]
program_lines = Parser.g.final_tree.root.children[-1].name[2]
for line in range(program_lines):
    l = [False, line+1]
    tf.append(l)

for i in range(len(post)):
    if post[i].name == 'var_decl':
        ID = None
        for j in post[i].children:
            if j.name[0] == 'keywords':
                keyword = j.name[1]
            if j.name[0] == 'ID':
                ID = j.name[1]
                mem_pos += 4
                instructions.append(pseudo_load_store('store', ID, mem_pos))
            if not ID:
                pass
            else:
                RAM[ID] = [mem_pos, 4]
    if post[i].name =='method_dec':
        instructions.append(pseudo_create_label('label_function', post[i].children[1].name[1]))
        args = len(post[i].children[3:-2])
        if len(post[i].children[3:-2]) == 2:
            instructions.append(pseudo_arith_logic('addi', 'sp', -4))
            instructions.append(pseudo_load_store('store', 'a0', '4(sp)'))
            instructions.append(pseudo_load_store('store', 'ra', '0(sp)'))
        if len(post[i].children[3:-2]) == 5:
            instructions.append(pseudo_arith_logic('addi', 'sp', -8))
            instructions.append(pseudo_load_store('store', 'a0', '8(sp)'))
            instructions.append(pseudo_load_store('store', 'a1', '4(sp)'))
            instructions.append(pseudo_load_store('store', 'ra', '0(sp)'))
        if len(post[i].children[3:-2]) == 8:
            instructions.append(pseudo_arith_logic('addi', 'sp', -12))
            instructions.append(pseudo_load_store('store', 'a0', '12(sp)'))
            instructions.append(pseudo_load_store('store', 'a1', '8(sp)'))
            instructions.append(pseudo_load_store('store', 'a2', '4(sp)'))
            instructions.append(pseudo_load_store('store', 'ra', '0(sp)'))
        
        if len(post[i].children[3:-2]) == 11:
            instructions.append(pseudo_arith_logic('addi', 'sp', -16))
            instructions.append(pseudo_load_store('store', 'a0', '16(sp)'))
            instructions.append(pseudo_load_store('store', 'a1', '12(sp)'))
            instructions.append(pseudo_load_store('store', 'a2', '8(sp)'))
            instructions.append(pseudo_load_store('store','a3', '4(sp)'))
            instructions.append(pseudo_load_store('store', 'ra', '0(sp)'))



    '''if post[i].name[1] == 'for':
        var1 = post[i].parent.children[1].name[1]
        var2 = literal_eval(getExprValue(post[i].parent.children[3], 'int'))
        var3 = post[i].parent.children[5].children[0].name[1]
        var4 = literal_eval(getExprValue(post[i].parent.children[5].children[2], 'int'))

        if post[i].parent.children[5].children[1].name[1] == '<':
            inst.insert(pseudo_branch('bl', var3, var4, 'label'))
            tf[post[i].parent.children[5].children[1].name[2]-1][0] = True

        if post[i].parent.children[5].children[1].name[1] == '>':
            inst.insert(pseudo_branch('bg', var3, var4, 'label'))
            tf[post[i].parent.children[5].children[1].name[2]-1][0] = True

        if post[i].parent.children[5].children[1].name[1] == '>=':
            inst.insert(pseudo_branch('bge', var3, var4, 'label'))
            tf[post[i].parent.children[5].children[1].name[2]-1][0] = True

        if post[i].parent.children[5].children[1].name[1] == '<=':
            inst.insert(pseudo_branch('ble', var3, var4, 'label'))
            tf[post[i].parent.children[5].children[1].name[2]-1][0] = True

        inst.insert(pseudo_load_store('load', var1, var2))'''
    
    if post[i].name[1] == 'for':
        instructions.append(pseudo_create_label('label', 'for'+str(for_label_counter)))
        for_labels.append('for'+str(for_label_counter))
        for_label_counter += 1

    if post[i].name[1] == '<':
        var1 = leftsibling(post[i]).name[1]
        var2 = eval(getExprValue(rightsibling(post[i]), 'int'))
        instructions.append(pseudo_branch('bg', var1, var2, for_labels[0]))

    if post[i].name[1] == '<=':
        var1 = leftsibling(post[i]).name[1]
        var2 = eval(getExprValue(rightsibling(post[i]), 'int'))
        instructions.append(pseudo_branch('bge', var1, var2, 'else_label'))

    if post[i].name[1] == '>':
        var1 = leftsibling(post[i]).name[1]
        var2 = eval(getExprValue(rightsibling(post[i]), 'int'))
        instructions.append(pseudo_branch('bl', var1, var2, 'else_label'))
        
    if post[i].name[1] == '>=':
        var1 = leftsibling(post[i]).name[1]
        var2 = eval(getExprValue(rightsibling(post[i]), 'int'))
        instructions.append(pseudo_branch('ble', var1, var2, 'else_label'))

    if post[i].name[1] == '=':
        if leftsibling(post[i]).name == 'location':
            var1 = leftsibling(post[i]).children[0].name[1]
        else :
            var1 = leftsibling(post[i]).name[1]
        var2 = eval(getExprValue(rightsibling(post[i]), 'int'))
        instructions.append(pseudo_load_store('load', var1, var2))

    if post[i].name[1] == '+=':
        var1 = leftsibling(post[i]).children[0].name[1]
        var2 = eval(getExprValue(rightsibling(post[i]), 'int'))
        instructions.append(pseudo_arith_logic('add', var1, var2))
    
    if post[i].name[1] == '-=':
        var1 = leftsibling(post[i]).children[0].name[1]
        var2 = eval(getExprValue(rightsibling(post[i]), 'int'))
        instructions.append(pseudo_arith_logic('sub', var1, var2))
    
    if post[i].name[1] == '==':
        var1 = leftsibling(post[i]).name[1]
        var2 = eval(getExprValue(rightsibling(post[i]), 'int'))
        if len(else_labels) == 0:
            label = 'endif'
        else:
            label = else_labels[0]
        instructions.append(pseudo_branch('bne', var1, var2, label))

    if post[i].name[1] == '!=':
        var1 = leftsibling(post[i]).name[1]
        var2 = eval(getExprValue(rightsibling(post[i]), 'int'))
        if len(else_labels) == 0:
            label = 'endif'
        else:
            label = else_labels[0]
        instructions.append(pseudo_branch('be', var1, var2, label))

    if post[i].name[1] == 'else':
        instructions.append(pseudo_create_label('label', 'else'+str(else_label_counter)))
    
    if post[i].name[1] == '||':
        var1 = eval(getExprValue(leftsibling(post[i]), 'int'))
        var2 = eval(getExprValue(rightsibling(post[i]), 'int'))
        instructions.append(pseudo_arith_logic('or', var1, var2))

    if post[i].name[1] == '&&':
        var1 = eval(getExprValue(leftsibling(post[i]), 'int'))
        var2 = eval(getExprValue(rightsibling(post[i]), 'int'))
        instructions.append(pseudo_arith_logic('and', var1, var2))
    
    if post[i].name[1] == 'for':
        for_index = i
        if block_index != None:
            print(post[block_index].name[1])
    
    if post[i].name == 'block':
        for x in post[i].siblings:
            if x.name[1] == 'for':
                block_index = i
                for g in post[block_index].children:
                    if g.name[1] == '}':
                        instructions.append(pseudo_jump('j', 'for_label'))
                        instructions.append(pseudo_create_label('label', 'endfor'))
            elif x.name[1] == 'if':
                if post[i].children[-1].name[1] == '}':
                    instructions.append(pseudo_create_label('label', 'endif'))
                #for g in post[i].children:
                 #   if g.name[1] == '}':
                  #      instructions.append(pseudo_create_label('label', 'endif'))
    
    if post[i].name[1] == 'break':
        instructions.append(pseudo_jump('j', 'endfor_label'))
    
    if post[i].name[1] == 'callout':
        strings.append(rightsibling(rightsibling(post[i])).name[1])
        instructions.append(pseudo_create_label('print', strings[0]))


    if post[i].name[1] == 'return':
        var1 = eval(getExprValue(rightsibling(post[i]), 'int'))
        if args == 2:
            instructions.append(pseudo_arith_logic('addi', 'sp', -4))
            instructions.append(pseudo_load_store('load', 'a0', '4(sp)'))
            instructions.append(pseudo_load_store('load', 'ra', '0(sp)'))
        if args == 5:
            instructions.append(pseudo_arith_logic('addi', 'sp', -8))
            instructions.append(pseudo_load_store('load', 'a0', '8(sp)'))
            instructions.append(pseudo_load_store('load', 'a1', '4(sp)'))
            instructions.append(pseudo_load_store('load', 'ra', '0(sp)'))
        if args == 8:
            instructions.append(pseudo_arith_logic('addi', 'sp', -12))
            instructions.append(pseudo_load_store('load', 'a0', '12(sp)'))
            instructions.append(pseudo_load_store('load', 'a1', '8(sp)'))
            instructions.append(pseudo_load_store('load', 'a2', '4(sp)'))
            instructions.append(pseudo_load_store('load', 'ra', '0(sp)'))
        
        if args == 11:
            instructions.append(pseudo_arith_logic('addi', 'sp', -16))
            instructions.append(pseudo_load_store('load', 'a0', '16(sp)'))
            instructions.append(pseudo_load_store('load', 'a1', '12(sp)'))
            instructions.append(pseudo_load_store('load', 'a2', '8(sp)'))
            instructions.append(pseudo_load_store('load','a3', '4(sp)'))
            instructions.append(pseudo_load_store('load', 'ra', '0(sp)'))
            
        instructions.append(pseudo_load_store('load', 't8', var1)) #t8 es el registro de returns
        instructions.append(pseudo_jump('j', 'ra'))
    
for g in range(len(instructions)-1, -1, -1):
    inst.insert(instructions[g])

inst.iterate()
with open('../code_gen/IRT.txt', 'a+') as f:
    for i in range(len(strings)):
        f.write('string'+str(i)+': .asciiz '+strings[i])
'''with open('IRT.txt', 'w') as f:
    f.write('.data \n')
    for x in range(len(strings)):
        f.write('   string'+str(x)+': '+ '.asciiz ' + strings[0])'''
