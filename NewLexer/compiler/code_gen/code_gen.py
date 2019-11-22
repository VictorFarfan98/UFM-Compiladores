import os
file = []

with open('IRT.txt', 'r') as f:
    for lines in f:
        file.append(lines.strip('\n'))
if os.path.exists('generated.s'):
    os.remove('generated.s')
mips = open('generated.s', 'a+')

def data():
    mips.write('.data\n '+file[-1]+'\n.text\n')

def end_file(file):
    file.write('   li $v0 10\n   syscall')

def label_function(array):
    for i in array:
        if 'label_function' in i:
            mips.write(i.split(' ')[1]+':\n')

def impreso(array):
    for x in file:
        if 'print' in x:
            prints = x.split(' ')
            mips.write('   li $v0 4\n   la $a0 string0\n   syscall\n\n')
data()
label_function(file)
impreso(file)
end_file(mips)

