.data 
    n: .word 0
    res: .word 0
    msg1:	.asciiz	"\n Enter a positive integer: " 

.text 
    main: 
        li $v0 4
        la $a0, msg1
        syscall

        li $v0, 5
        syscall
        sw $v0, ($sp)
        add $sp, $sp, 4
        

    factorial: 
