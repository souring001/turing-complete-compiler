OP_PUSH2
OP_PUSH3
OP_PUSH4
OP_PUSH5
OP_PUSH .L0
OP_PUSH 9
OP_CALL .L_fib
.label .L0
OP_POP1
OP_POP5
OP_POP4
OP_POP3
OP_POP2
OP_PUSH1
OP_POP7
.label .L_fib
OP_POP2
OP_PUSH2
OP_PUSH 0
OP_JEQ .L2
OP_PUSH2
OP_PUSH 1
OP_JEQ .L4
OP_PUSH2
OP_PUSH3
OP_PUSH4
OP_PUSH5
OP_PUSH .L5
OP_PUSH2
OP_PUSH 1
OP_SUB
OP_CALL .L_fib
.label .L5
OP_POP1
OP_POP5
OP_POP4
OP_POP3
OP_POP2
OP_PUSH1
OP_PUSH2
OP_PUSH3
OP_PUSH4
OP_PUSH5
OP_PUSH .L6
OP_PUSH2
OP_PUSH 2
OP_SUB
OP_CALL .L_fib
.label .L6
OP_POP1
OP_POP5
OP_POP4
OP_POP3
OP_POP2
OP_PUSH1
OP_ADD
OP_SWAP
OP_RET
OP_JMP .L3
.label .L4
.label .L3
OP_JMP .L1
.label .L2
.label .L1
OP_PUSH 1
OP_SWAP
OP_RET
