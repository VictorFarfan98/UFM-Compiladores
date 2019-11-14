import shlex
import sys, getopt, argparse, os

HFA = {0:{'-':5, '0':1, '1':3, '2':3, '3':3, '4':3, '5':3, '6':3, '7':3, '8':3, '9':3},
		1:{'x':2},
		2:{'a':2, 'b':2, 'c':2, 'd':2, 'e':2, 'f':2, 'A':2, 'B':2, 'C':2, 'D':2, 'E':2, 'F':2, '0':2, '1':2, '2':2, '3':2, '4':2, '5':2, '6':2, '7':2, '8':2, '9':2},
		3:{'.':4, '0':3, '1':3, '2':3, '3':3, '4':3, '5':3, '6':3, '7':3, '8':3, '9':3},
		4:{'0':4, '1':4, '2':4, '3':4, '4':4, '5':4, '6':4, '7':4, '8':4, '9':4},
		5:{'0':6, '1':8, '2':8, '3':8, '4':8, '5':8, '6':8, '7':8, '8':8, '9':8},
		6:{'x':7},
		7:{'a':7, 'b':7, 'c':7, 'd':7, 'e':7, 'f':7, 'A':7, 'B':7, 'C':7, 'D':7, 'E':7, 'F':7, '0':7, '1':7, '2':7, '3':7, '4':7, '5':7, '6':7, '7':7, '8':7, '9':7},
		8:{'.':9, '0':8, '1':8, '2':8, '3':8, '4':8, '5':8, '6':8, '7':8, '8':8, '9':8},
		9:{'0':9, '1':9, '2':9, '3':9, '4':9, '5':9, '6':9, '7':9, '8':9, '9':9}}

SFA = {0:{34:1},
	   1:{34:3, 92:2, 32:1, 33:1, 35:1, 36:1, 37:1, 38:1, 40:1, 41:1, 42:1, 43:1, 44:1, 45:1, 46:1, 47:1, 48:1, 49:1, 50:1, 51:1, 52:1, 53:1, 54:1, 55:1, 56:1, 57:1, 58:1, 59:1, 60:1, 61:1, 62:1, 63:1, 64:1, 65:1, 66:1, 67:1, 68:1, 69:1, 70:1, 71:1,
	    72:1, 73:1, 74:1, 75:1, 76:1, 77:1, 78:1, 79:1, 80:1, 81:1, 82:1, 83:1, 84:1, 85:1, 86:1, 87:1, 88:1, 89:1, 90:1, 91:1, 93:1, 94:1, 95:1, 96:1, 97:1, 98:1, 99:1, 100:1, 101:1, 102:1, 103:1, 104:1, 105:1, 106:1, 107:1, 108:1, 109:1, 110:1, 111:1, 
		112:1, 113:1, 114:1, 115:1, 116:1, 117:1, 118:1, 119:1, 120:1, 121:1, 123:1, 124:1, 125:1, 126:1},
	   2:{39:1, 34:1, 92:1, 110:1, 116:1},
	   3:{}}



CFA = {0:{'(':1, ')':1, '[':1, ']':1, '{':1, '}':1, ',':1, ';':1},
	   1:{}}

EFA = {0:{';':1},
	   1:{}}

OFA = {0:{'<':2, '=':1, '>':2, '+':2, '-':2, '/':1, '*':1, '%':1, '^':1, '!':2},
	   1:{},
	   2:{'=':1, '':1}}

SCFA = {0:{39:1},
	   1:{39:2, 32:1, 33:1, 35:1, 36:1, 37:1, 38:1, 40:1, 41:1, 42:1, 43:1, 44:1, 45:1, 46:1, 47:1, 48:1, 49:1, 50:1, 51:1, 52:1, 53:1, 54:1, 55:1, 56:1, 57:1, 58:1, 59:1, 60:1, 61:1, 62:1, 63:1, 64:1, 65:1, 66:1, 67:1, 68:1, 69:1, 70:1, 71:1, 72:1, 73:1, 74:1, 75:1, 76:1, 77:1, 78:1, 79:1, 80:1, 81:1, 82:1, 83:1, 84:1, 85:1, 86:1, 87:1, 88:1, 89:1, 90:1, 91:1, 93:1, 94:1, 95:1, 96:1, 97:1, 98:1, 99:1, 100:1, 101:1, 102:1, 103:1, 104:1, 105:1, 106:1, 107:1, 108:1, 109:1, 110:1, 111:1, 112:1, 113:1, 114:1, 115:1, 116:1, 117:1, 118:1, 119:1, 120:1, 121:1, 123:1, 124:1, 125:1, 126:1},
	   2:{}}

ID = {0:{'A':1, 'B':1, 'C':1, 'D':1, 'E':1, 'F':1, 'G':1, 'H':1, 'I':1, 'J':1, 'K':1, 'L':1, 'M':1, 'N':1, 'O':1, 'P':1, 'Q':1, 'R':1, 'S':1, 'T':1, 'U':1, 'V':1, 'W':1, 'X':1, 'Y':1, 'Z':1, '_':1, 'a':1, 'b':1, 'c':1, 'd':1, 'e':1, 'f':1, 'g':1, 'h':1, 'i':1, 'j':1, 'k':1, 'l':1, 'm':1, 'n':1, 'o':1, 'p':1, 'q':1, 'r':1, 's':1, 't':1, 'u':1, 'v':1, 'w':1, 'x':1, 'y':1, 'z':1},
	  1:{'A':1, 'B':1, 'C':1, 'D':1, 'E':1, 'F':1, 'G':1, 'H':1, 'I':1, 'J':1, 'K':1, 'L':1, 'M':1, 'N':1, 'O':1, 'P':1, 'Q':1, 'R':1, 'S':1, 'T':1, 'U':1, 'V':1, 'W':1, 'X':1, 'Y':1, 'Z':1, '_':1, 'a':1, 'b':1, 'c':1, 'd':1, 'e':1, 'f':1, 'g':1, 'h':1, 'i':1, 'j':1, 'k':1, 'l':1, 'm':1, 'n':1, 'o':1, 'p':1, 'q':1, 'r':1, 's':1, 't':1, 'u':1, 'v':1, 'w':1, 'x':1, 'y':1, 'z':1, '0':1, '1':1, '2':1, '3':1, '4':1, '5':1, '6':1, '7':1, '8':1, '9':1}}

def type(listt, types):
	matrix = []
	y = 0
	for x in listt:
		aceptado = False
		lists = [None, None]
		if x in types['keywords']:
			lists[0] = 'keywords'
			lists[1] = x
			matrix.append(lists)
		else:
			try:
				if accepts(HFA, 0, {2, 3, 4, 7, 8, 9, 1}, x) in (2, 7):
					if listt[y-1] == '-':
						x = '-' + x
					lists[0] = 'hexadecimal'
					lists[1] = x
					matrix.append(lists)
					aceptado = True				
				if accepts(HFA, 0, {2, 3, 4, 7, 8, 9, 1}, x) in (3, 4, 8, 9):
					if listt[y-1] == '-':
						x = '-' + x
					if listt[y+1] == '.':
						x = x + '.' + listt[y+2]
					lists[0] = 'decimal'
					lists[1] = x
					matrix.append(lists)
					aceptado = True
			except:
				pass
			try:
				if accepts(ID, 0, {1}, x):
					lists[0] = 'ID'
					lists[1] = x
					matrix.append(lists)
					aceptado = True
			except:
				pass
			try:
				if accepts(CFA, 0, {1}, x):
					lists[0] = 'Delimiter'
					lists[1] = x
					matrix.append(lists)
					aceptado = True
			except:
				pass
			""" Try that set End of instruction as type
			try:
				if accepts(EFA, 0, {1}, x):
					lists[0] = 'End of instruction'
					lists[1] = x
					matrix.append(lists)
					aceptado = True
			except:
				pass
			"""
			try:
				if accepts(OFA, 0, {1}, x):
					if listt[y+1] == '=':
						x = x + '='
					if listt[y-1] in ('-', '+', '<', '>'):
						pass
					else:
						lists[0] = 'Operator'
						lists[1] = x
						matrix.append(lists)
					aceptado = True
			except:
				pass
			try:
				if x[0] == '"':
					if accepts_string(SFA, 0, {3}, x):
						lists[0] = 'string'
						lists[1] = x
						matrix.append(lists)
						aceptado = True
				elif x[0] == "'":
					if accepts_string(SCFA, 0, {2}, x):
						lists[0] = 'char'
						lists[1] = x
						matrix.append(lists)
						aceptado = True
			except:
				pass
			if aceptado == False:
				if x == '0':
					lists[0] = 'decimal'
					lists[1] = x
				#print("Unexpected token: ", x)
				else:
					lists[0] = 'Unexpected token'
					lists[1] = x
				matrix.append(lists)
		y += 1
	return matrix 

escape_dict={'\a':r'\a',
           '\b':r'\b',
           '\c':r'\c',
           '\f':r'\f',
           '\n':r'\n',
           '\r':r'\r',
           '\t':r'\t',
           '\v':r'\v',
           '\'':r'\'',
           '\"':r'\"',
           '\0':r'\0',
           '\1':r'\1',
           '\2':r'\2',
           '\3':r'\3',
           '\4':r'\4',
           '\5':r'\5',
           '\6':r'\6',
           '\7':r'\7',
		   '\8':r'\8',
           '\9':r'\9',
           '\\':r'\\'}

def raw(text):
    """Returns a raw string representation of text"""
    new_string='"'
    for char in text:
        try:
        	new_string+=escape_dict[char]
        except KeyError: 
        	new_string+=char
    new_string+='"'  
    return new_string
	
newlist_location = []
def tokenize(file, newlist_location):
	with open(file, 'r') as f:
		location = 1
		newlist = []
		try:	
			for line in f:
				newlist_location.append([line, location])
				str = list(shlex.shlex(line))
				newlist.extend(str)
				location += 1
		except ValueError:
			print('Syntax Error. No closing quotation')
		newlist_location = newlist
	return newlist

def accepts(transitions,initial,accepting,s):
    state = initial
    for c in s:
        state = transitions[state][c]
    return state

def accepts_string(transitions,initial,accepting,s):
    state = initial
    for c in s:
        state = transitions[state][ord(c)]
    return state in accepting

ap = argparse.ArgumentParser()
ap.add_argument("file", help="Inputfile")
ap.add_argument("-debug", required=False, help="<stage>: [scan, parse, ast, semantic, irt, codegen] ")
args = vars(ap.parse_args())

tofile = []
keywords = {'keywords':['boolean', 'break', 'callout', 'class', 'continue', 'else', 'false', 'for', 'if', 'int', 'return', 'void', 'true', 'print', 'String']}
newlist = tokenize("../"+str(args["file"]), newlist_location)
#print(newlist)
newlist = type(newlist, keywords)

signs = ['<','>','!','+','-']
for line in newlist_location:
	line[0] = list(shlex.shlex(line[0]))

curtoken = 0
for location in newlist_location:
	#print(location)
	if len(location[0]) > 0:
		for i in range(len(location[0])):
			#print(location[0][i])
			if location[0][i] == "=":
				if location[0][i-1] in signs:
					curtoken -= 1
			if len(newlist[curtoken]) != 3:
				newlist[curtoken].append(location[1])
			curtoken += 1
			#print(curtoken)

if args["debug"] == None:
	for element in newlist:
		if element[0] == "Unexpected token":
			print(element)
		elif element[0] != "Unexpected token":
			tofile.append(str(element))
else:
	for element in newlist:
		if element[0] != "Unexpected token":
			print(element)
			tofile.append(str(element))

#print(tofile)
print(os.getcwd())
#outF = open("../parser/token.txt", "w")
#outF.writelines(tofile)
#outF.close()

curlocation = 0
"""
for i in range(len(newlist)):
	print("old", newlist[i])
	if newlist[i][1] in newlist_location[curlocation][0]:
		newlist[i].append(newlist_location[curlocation][1])
	else:
		curlocation += 1		
		i -= 1
	print(newlist[i])
"""

outF = open("../parser/token.txt", "w")
for line in tofile:
	outF.write(line)
	outF.write("\n")
outF.close()

outF = open("../semantic check/token.txt", "w")
for line in tofile:
	outF.write(line)
	outF.write("\n")
outF.close()

outF = open("../irt/token.txt", "w")
for line in tofile:
	outF.write(line)
	outF.write("\n")
outF.close()

with open("location.txt", "w") as l:
	for i in newlist_location:
		l.write(str(i))
		l.write('\n')