from ast import literal_eval
import sys
import pickle
from anytree import Node, RenderTree
from anytree.dotexport import RenderTreeGraph
from anytree.exporter import DotExporter
from graphviz import Source
from graphviz import render
from graphviz import Graph

class Grammar:
    def __init__(self):
        self.tokens = []
        self.tree = []
        self.final_tree = None
        self.parent = None
        self.subtree = None
        self.subparent = None
        self.newtokens = []
        with open("token.txt", 'r') as f:
            for line in f:
                line = literal_eval(line)
                self.tokens.append(line)
    
    def getType(self, token):
        return token[0]

    def getValue(self, token):
        return token[1]

    def ignoreToken(self):
        popped = self.tokens.pop(0)

    def popToken(self, nodo, padre=None):
        popped = self.tokens.pop(0)
        popped.append(nodo)
        if padre != None:
            self.child = Node(popped, parent=padre)
        self.tree.append(popped)
        self.newtokens.append(popped)
        print("Popped:", popped)

    def printExpectedToken(self, expected):
        print("Expected Token: "+expected+", found ", self.tokens[0], "instead. Near line:", (self.tokens[0][2]))
        sys.exit()

    def isexpected(self, token, tipo, value):
        return self.getType(token) == tipo and self.getValue(token) == value

    def istype(self, token):
        return self.isexpected(token, "keywords", "int") or self.isexpected(token, "keywords", "boolean")

    def isID(self, token):
        return self.getType(token) == "ID"

    def syntaxProgram(self):
        arbol = Node('program')         
        if self.isexpected(self.tokens[0], "keywords", "class"):
            self.popToken('program', arbol)
            if self.isexpected(self.tokens[0], "ID", "Program"):
                self.popToken('program', arbol)    
                if self.isexpected(self.tokens[0], "Delimiter", "{"):
                    self.popToken('program', arbol)  
                    if not self.isexpected(self.tokens[0], "Delimiter", "}"):  
                        try:
                            while self.isexpected(self.tokens[2], "Delimiter", "["):
                                self.syntaxField_dec(self.subtree, arbol)
                            while self.isexpected(self.tokens[2], "Delimiter", "("):
                                self.syntaxMethod_dec(self.subtree, arbol)
                        except IndexError:
                            pass
                    if self.isexpected(self.tokens[0], "Delimiter", "}"):
                        self.popToken('program', arbol)
                        print("Program OK")
                    else:
                        self.printExpectedToken("['Delimiter', '}']")
                else:
                    self.printExpectedToken("['Delimiter', '{']")
            else:
                self.printExpectedToken("['ID', 'Program']")
        else:
            self.printExpectedToken("['keywords', 'class']")
        self.final_tree = arbol

    def syntaxField_dec(self, subtree, arbol):
        subtree = Node('Field_dec')

        while self.istype(self.tokens[0]):
            self.popToken('field_dec', subtree)   
            if self.isexpected(self.tokens[1], "Delimiter", "["):
                if self.isID(self.tokens[0]):
                    self.popToken('field_dec', subtree) 
                    if self.isexpected(self.tokens[0], "Delimiter", "["):
                        self.popToken('field_dec', subtree) 
                        if self.getType(self.tokens[0]) == "decimal" or self.getType(self.tokens[0]) == "hexadecimal":
                            self.popToken('field_dec', subtree)    
                            if self.isexpected(self.tokens[0], "Delimiter", "]"):
                                self.popToken('field_dec', subtree)
                                if self.isexpected(self.tokens[0], "Delimiter", ","):
                                    self.popToken('field_dec', subtree)
                                    continue
                                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                                    self.popToken('field_dec', subtree)
                                    break
                                else:
                                    self.printExpectedToken("['Delimiter',';']")
                            else:
                                self.printExpectedToken("['Delimiter', ']']")
                        else:
                            if self.getType(self.tokens[1]) == "decimal" or self.getType(self.tokens[0]) == "hexadecimal":
                                self.ignoreToken()
                                if self.getType(self.tokens[0]) == "decimal" or self.getType(self.tokens[0]) == "hexadecimal":
                                    self.popToken('field_dec', subtree)    
                                    if self.isexpected(self.tokens[0], "Delimiter", "]"):
                                        self.popToken('field_dec', subtree)
                                        if self.isexpected(self.tokens[0], "Delimiter", ","):
                                            self.popToken('field_dec', subtree)
                                            continue
                                        if self.isexpected(self.tokens[0], "Delimiter", ";"):
                                            self.popToken('field_dec', subtree)
                                            break
                                        else:
                                            self.printExpectedToken("['Delimiter',';']")
                                    else:
                                        self.printExpectedToken("['Delimiter', ']']")
                            else:    
                                self.printExpectedToken("<int_literal>")

                    else:
                        self.printExpectedToken("['Delimiter', '[']")
                else:
                    self.printExpectedToken("<ID>")    
            elif self.getType(self.tokens[0]) == "ID":
                self.popToken('field_dec', subtree)
                if self.isexpected(self.tokens[0], "Delimiter", ","):
                    self.popToken('field_dec', subtree)
                    continue
                elif self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken('field_dec', subtree)
                    break
                else:
                    self.printExpectedToken("['Delimiter',';']")
            else:
                self.printExpectedToken("<ID>")
        """
        if self.istype(self.tokens[0]):
            self.popToken('field_dec', subtree)      
            while True:
                if self.getType(self.tokens[0]) == "ID":
                    self.popToken('field_dec', subtree)    
                    if self.isexpected(self.tokens[0], "Delimiter", "["):
                        self.popToken('field_dec', subtree)    
                        if self.getType(self.tokens[0]) == "decimal" or self.getType(self.tokens[0]) == "hexadecimal":
                            self.popToken('field_dec', subtree)    
                            if self.isexpected(self.tokens[0], "Delimiter", "]"):
                                self.popToken('field_dec', subtree)    
                            else:
                                self.printExpectedToken("['Delimiter', ']']")
                        else:
                            self.printExpectedToken("<int_literal>")
                    elif self.isexpected(self.tokens[0], "Delimiter", ","):
                        self.popToken('field_dec', subtree)    
                        continue
                    elif self.isexpected(self.tokens[0], "Delimiter", ";"):
                        self.popToken('field_dec', subtree)    
                        break
                    else:
                        self.printExpectedToken("['Delimiter', ';']")
                else:
                    self.printExpectedToken("['ID', '*']")
        else:
            self.printExpectedToken("<type>")
        subtree.parent = arbol
        """


    def syntaxMethod_dec(self, subtree, arbol): #Could fail due to while statement  
        subtree = Node('method_dec')      
        if self.istype(self.tokens[0]) or self.isexpected(self.tokens[0], "keywords", "void"):
            print("meth dec")
            self.popToken('method_dec', subtree)    
            if self.isID(self.tokens[0]):
                self.popToken('method_dec', subtree)    
                if self.isexpected(self.tokens[0], "Delimiter", "("):
                    self.popToken('method_dec', subtree)    
                    if self.istype(self.tokens[0]):
                        while self.istype(self.tokens[0]):
                            if self.istype(self.tokens[0]):
                                self.popToken('method_dec', subtree)    
                                if self.isID(self.tokens[0]):
                                    self.popToken('method_dec', subtree)    
                                    if self.isexpected(self.tokens[0], "Delimiter", ","):
                                        self.popToken('method_dec', subtree)    
                                        continue
                                    elif self.isexpected(self.tokens[0], "Delimiter", ")"):
                                        self.popToken('method_dec', subtree)    
                                        self.syntaxBlock(subtree)
                                        break
                                    else:
                                        self.printExpectedToken("['Delimiter', ')']")
                                else:
                                    self.printExpectedToken("<ID>")
                            else:
                                self.printExpectedToken("<type>")
                    elif self.isexpected(self.tokens[0], "Delimiter", ")"):
                        self.popToken('method_dec', subtree)
                        self.syntaxBlock(subtree)
                    else:
                        self.printExpectedToken("['Delimiter',')']")
                else:
                    self.printExpectedToken("['Delimiter', '(']")
            else:
                self.printExpectedToken("<ID>")
        else:
            self.printExpectedToken("<method type>")
        subtree.parent = arbol
    
    def syntaxBlock(self, herencia=None):    
        new_tree = Node('block')    
        if self.isexpected(self.tokens[0], "Delimiter", "{"):
            self.popToken('block', new_tree)            
            self.syntaxVar_decl(new_tree)
            self.syntaxStatement(new_tree)
            if self.isexpected(self.tokens[0], "Delimiter", "}"):
                self.popToken('block', new_tree)
            else:
                self.printExpectedToken("['Delimiter','}']")
        else:
            self.printExpectedToken("['Delimiter', '{']")
        new_tree.parent = herencia

    def syntaxVar_decl(self, herencia=None): 
        new_tree = Node('var_decl')       
        while self.istype(self.tokens[0]):
            self.popToken('var_decl', new_tree)
            if self.isID(self.tokens[0]):
                self.popToken('var_decl', new_tree)
                while self.isexpected(self.tokens[0], "Delimiter", ","):
                    self.popToken('var_decl', new_tree)
                    if self.isID(self.tokens[0]):
                        self.popToken('var_decl', new_tree)
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken('var_decl', new_tree)
                else:
                    self.printExpectedToken("['Delimiter',';']")
            else:
                self.printExpectedToken("<ID>")
        new_tree.parent = herencia        

    """
    def syntaxType(self):
        pass
    """
    def syntaxStatement(self, herencia=None):
        new_tree = Node('statement')
        while not self.isexpected(self.tokens[0], "Delimiter", "}"):
            if (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", "(")) or self.isexpected(self.tokens[0], "keywords", "callout"):
                #is method_call
                self.syntaxMethod_call(new_tree)
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken('statement', new_tree)
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isID(self.tokens[0]) or (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", "[")):
                #is location
                self.syntaxLocation(new_tree)
                if self.isAssignOp(self.tokens[0]):
                    self.popToken('statement', new_tree)
                    self.syntaxExpr(new_tree)
                    if self.isexpected(self.tokens[0], "Delimiter", ";"):
                        self.popToken('statement', new_tree)
                    else:
                        self.printExpectedToken("['Delimiter',';']")
                else:
                    self.printExpectedToken("<assig_op>")
            elif self.isexpected(self.tokens[0], "keywords", "if"):
                #is if
                self.popToken('statement', new_tree)
                if self.isexpected(self.tokens[0], "Delimiter", "("):
                    self.popToken('statement', new_tree)
                    self.syntaxExpr(new_tree)
                    if self.isexpected(self.tokens[0], "Delimiter", ")"):
                        self.popToken('statement', new_tree)
                        self.syntaxBlock(new_tree)
                        if self.isexpected(self.tokens[0], "keywords", "else"):
                            self.popToken('statement', new_tree)
                            self.syntaxBlock(new_tree)
                    else:
                        self.printExpectedToken("['Delimiter',')']")
                else:
                    self.printExpectedToken("['Delimiter','(']")
            elif self.isexpected(self.tokens[0], "keywords", "for"):
                #is for
                self.popToken('statement', new_tree)
                if self.isID(self.tokens[0]):
                    self.popToken('statement', new_tree)
                    if self.isexpected(self.tokens[0], "Operator", "="):
                        self.popToken('statement', new_tree)
                        self.syntaxExpr(new_tree)
                        if self.isexpected(self.tokens[0], "Delimiter", ","):
                            self.popToken('statement', new_tree)
                            self.syntaxExpr(new_tree)
                            self.syntaxBlock(new_tree)
                        else:
                            self.printExpectedToken("['Delimiter',',']")
                    else:
                        self.printExpectedToken("['Operator','=']")
                else:
                    self.printExpectedToken("<ID>")
            elif self.isexpected(self.tokens[0], "keywords", "return"):
                #is return
                self.popToken('statement', new_tree)
                self.syntaxExpr(new_tree)
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken('statement', new_tree)
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isexpected(self.tokens[0], "keywords", "break"):
                #is break
                self.popToken('statement', new_tree)
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken('statement', new_tree)
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isexpected(self.tokens[0], "keywords", "continue"):
                #is continue
                self.popToken('statement', new_tree)
                if self.isexpected(self.tokens[0], "Delimiter", ";"):
                    self.popToken('statement', new_tree)
                else:
                    self.printExpectedToken("['Delimiter',';']")
            elif self.isexpected(self.tokens[0], "Delimiter", "{"):
                #is block
                self.syntaxBlock(new_tree)
            else:
                self.printExpectedToken("<statement>")
        new_tree.parent = herencia 
        
    def syntaxMethod_call(self, herencia=None):
        new_tree = Node('method_call')        
        if self.isID(self.tokens[0]):
            self.popToken('method_call', new_tree)
            if self.isexpected(self.tokens[0], "Delimiter", "("):
                self.popToken('method_call', new_tree)
                if not self.isexpected(self.tokens[0], "Delimiter", ")"):                    
                    self.syntaxExpr(new_tree)
                    
                    while self.isexpected(self.tokens[0], "Delimiter", ","):                        
                        self.popToken('method_call', new_tree)
                        self.syntaxExpr(new_tree)
                if self.isexpected(self.tokens[0], "Delimiter", ")"):
                    self.popToken('method_call', new_tree)
                else:
                    self.printExpectedToken("['Delimiter',')']")
            else:
                self.printExpectedToken("['Delimiter','(']")
        elif self.isexpected(self.tokens[0], "keywords", "callout"):
            self.popToken('method_call', new_tree)
            if self.isexpected(self.tokens[0], "Delimiter", "("):
                self.popToken('method_call', new_tree)
                if self.isStringLiteral(self.tokens[0]):
                    self.popToken('method_call', new_tree)
                    if self.isexpected(self.tokens[0], "Delimiter", ","):
                        self.syntaxCallout_arg()
                        while self.isexpected(self.tokens[0], "Delimiter", ","):
                            self.popToken('method_call', new_tree)
                            self.syntaxCallout_arg()
                        if self.isexpected(self.tokens[0], "Delimiter", ")"):
                            self.popToken('method_call', new_tree)
                        else:
                            self.printExpectedToken("['Delimiter',')']")
                    elif self.isexpected(self.tokens[0], "Delimiter", ")"):
                        self.popToken('method_call', new_tree)
                    else:
                        self.printExpectedToken("['Delimiter',')']")
                else:
                    self.printExpectedToken("<string_literal>")
            else:
                self.printExpectedToken("['Delimiter','(']")
        else:
            self.printExpectedToken("<method_name> or <callout>")
        new_tree.parent = herencia
    """
    def syntaxMethod_name(self):
        pass
    """

    def syntaxLocation(self, herencia=None):
        new_tree = Node('location')
        if self.isID(self.tokens[0]):
            self.popToken('location', new_tree)
            if self.isexpected(self.tokens[0], "Delimiter", "["):
                self.popToken('location', new_tree)
                self.syntaxExpr(new_tree)
                if self.isexpected(self.tokens[0], "Delimiter", "]"):
                    self.popToken('location', new_tree)
                else:
                    self.printExpectedToken("['Delimiter',']']")
        else:
            self.printExpectedToken("<ID>")
        new_tree.parent = herencia

    def syntaxExpr(self, herencia=None):
        new_tree = Node('expr')                
        if self.isBinOp(self.tokens[1]):
            #is expr alone
            self.popToken('expr', new_tree)
            
            if self.isBinOp(self.tokens[0]):
                self.popToken('expr', new_tree)
                self.syntaxExpr(new_tree)
            else:
                self.printExpectedToken("<bin_op>")
        elif (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", "(")) or self.isexpected(self.tokens[0], "keywords", "callout"):
            #is method_call                       
            self.syntaxMethod_call(new_tree)
        
        elif (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", ",")) or (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", ")")) or (self.isID(self.tokens[0]) and self.isexpected(self.tokens[1], "Delimiter", "[")):
            #is location
            print("is location")
            self.syntaxLocation(new_tree)
        elif self.isLiteral(self.tokens[0]):
            self.popToken('expr', new_tree)
        elif self.isexpected(self.tokens[0], "Operator", "-"):
            #is negative
            self.popToken('expr', new_tree)
            self.syntaxExpr(new_tree)
        elif self.isexpected(self.tokens[0], "Operator", "!"):
            #is differemt !
            self.popToken('expr', new_tree)
            self.syntaxExpr(new_tree)
        elif self.isexpected(self.tokens[0], "Delimiter", "("):
            #is parenthesis expr
            self.popToken('expr', new_tree)
            self.syntaxExpr(new_tree)
            if self.isexpected(self.tokens[0], "Delimiter", ")"):
                self.popToken('expr', new_tree)
            else:
                self.printExpectedToken("['Delimiter',')']")        
        else:
            self.printExpectedToken("<expr>")            
        new_tree.parent = herencia

    def syntaxCallout_arg(self, herencia=None):
        new_tree = Node('callout_arg')        
        if self.isStringLiteral(self.tokens[0]):
            self.popToken('callout_arg', new_tree)
        else:
            self.syntaxExpr(new_tree)
        new_tree.parent = herencia

    def syntaxBinOp(self, herencia=None):
        new_tree = Node('bin_op')
        if self.isBinOp(self.tokens[0]):
            self.popToken('bin_op', new_tree)
        else:
            self.printExpectedToken("<bin_op>")
        new_tree.parent = herencia
        

    def isAssignOp(self, token):
        return self.isexpected(token, "Operator", "=") or self.isexpected(token, "Operator", "+=") or self.isexpected(token, "Operator", "-=")

    def isBinOp(self, token):
        return self.isArithOp(token) or self.isRelOp(token) or self.isEqOp(token) or self.isCondOp(token)

    def isArithOp(self, token):
        return self.isexpected(token, "Operator", "+") or self.isexpected(token, "Operator", "-") or self.isexpected(token, "Operator", "*") or self.isexpected(token, "Operator", "/") or self.isexpected(token, "Operator", "%")

    def isRelOp(self, token):
        return self.isexpected(token, "Operator", "<") or self.isexpected(token, "Operator", ">") or self.isexpected(token, "Operator", "<=") or self.isexpected(token, "Operator", ">=")

    def isEqOp(self, token):
        return self.isexpected(token, "Operator", "==") or self.isexpected(token, "Operator", "!=")

    def isCondOp(self, token):
        return self.isexpected(token, "Operator", "&&") or self.isexpected(token, "Operator", "||")

    def isLiteral(self, token):
        return self.isIntLiteral(token) or self.isCharLiteral(token) or self.isBoolLiteral(token)
    
    """
    def syntaxId(self):
        pass
    """

    """
    def syntaxAlpha_num(self):
        pass
    """

    """
    def syntaxAlpha(self):
        pass
    """

    """
    def syntaxDigit(self):
        pass
    """

    """
    def syntaxHex_digit(self):
        pass
    """

    def isIntLiteral(self, token):
        return self.isDecimalLiteral(token) or self.isHexLiteral(token)

    def isDecimalLiteral(self, token):
        return self.getType(token) == "decimal"

    def isHexLiteral(self, token):
        return self.getType(token) == "hexadecimal"

    def isBoolLiteral(self, token):
        return (self.getType(token) == "keywords" and self.getValue(token) == "true") or (self.getType(token) == "keywords" and self.getValue(token) == "false")

    def isCharLiteral(self, token):
        return self.getType(token) == "char"

    def isStringLiteral(self, token):
        return self.getType(token) == "string"

    
g = Grammar()
#print(g.tokens)

g.syntaxProgram()
#print(RenderTree(g.final_tree))
tofile = g.newtokens

for pre, fill, node in RenderTree(g.final_tree):
    print("%s%s" % (pre, node.name))

outF = open("../semantic check/token.txt", "w")
for line in tofile:
	outF.write(str(line))
	outF.write("\n")
outF.close()

outF = open("../irt/token.txt", "w")
for line in tofile:
	outF.write(str(line))
	outF.write("\n")
outF.close()


#DotExporter(g.final_tree).to_dotfile("ast.dot")
#Source.from_file('ast.dot')

#DotExporter(g.final_tree).to_dotfile('../ast/udo.dot')
#Source.from_file('../ast/udo.dot')
#render('dot', 'png', '../ast/udo.dot') 
"""
render('dot', 'png', 'ast.dot') 
#RenderTreeGraph(g.final_tree).to_picture("ast.png")

"""
#dot.render(dot.render('test-output/round-table.gv', view=True)  )

# graphviz needs to be installed for the next line!
#DotExporter(g.final_tree).to_picture('../ast/ast.dot')
