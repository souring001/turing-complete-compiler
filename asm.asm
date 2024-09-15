# push .L0
mov .L0 0 r0
push r0 0 0
# push 9
mov 9 0 r0
push r0 0 0
# call
mov .L_fib 0 cnt
label .L0
pop 0 0 r1
push r1 0 0
pop 0 0 r5
label exit
mov exit 0 cnt

label .L_fib
pop 0 0 r2
# jeq
jeq r2 r3 .L2
push r2 0 0
# push 1
mov 1 0 r0
push r0 0 0
# jeq
pop 0 0 r0
pop 0 0 r1
jeq r1 r0 .L4
push r2 0 0
# push .L5
mov .L5 0 r0
push r0 0 0
push r2 0 0
# push 1
mov 1 0 r0
push r0 0 0
# sub
pop 0 0 r0
pop 0 0 r1
sub r1 r0 r1
push r1 0 0
# call
mov .L_fib 0 cnt
label .L5
pop 0 0 r1
pop 0 0 r2
push r1 0 0
push r2 0 0
# push .L6
mov .L6 0 r0
push r0 0 0
push r2 0 0
# push 2
mov 2 0 r0
push r0 0 0
# sub
pop 0 0 r0
pop 0 0 r1
sub r1 r0 r1
push r1 0 0
# call
mov .L_fib 0 cnt
label .L6
pop 0 0 r1
pop 0 0 r2
push r1 0 0
# add
pop 0 0 r0
pop 0 0 r1
add r1 r0 r1
push r1 0 0
# swap
pop 0 0 r0
pop 0 0 r1
push r0 0 0
push r1 0 0
# ret
pop 0 0 cnt
# jmp
mov .L3 0 cnt
label .L4
label .L3
# jmp
mov .L1 0 cnt
label .L2
label .L1
# push 1
mov 1 0 r0
push r0 0 0
# swap
pop 0 0 r0
pop 0 0 r1
push r0 0 0
push r1 0 0
# ret
pop 0 0 cnt
