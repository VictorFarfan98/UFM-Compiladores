.data
 string0: .asciiz "\tThis is my program!\n"
.text
main:
   li $v0 4
   la $a0 string0
   syscall

   li $v0 10
   syscall