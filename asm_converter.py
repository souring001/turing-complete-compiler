import re
file_name = 'fib.asm'

with open(file_name, 'r') as file:
    commands = [line.strip().split() for line in file]

for command in commands:
    # print(command)
    if command[0] == 'OP_PUSH':
        print(f'# push {command[1]}')
        print(f'mov {command[1]} 0 r0')
        print(f'push r0 0 0')
    elif match := re.match(r'^OP_PUSH([0-7])$', command[0]):
        rnum = match.group(1)
        print(f'push r{rnum} 0 0')
    elif command[0] == 'OP_POP':
        print('# pop only')
        print(f'pop 0 0 r0')
    elif match := re.match(r'^OP_POP([0-7])$', command[0]):
        rnum = match.group(1)
        print(f'pop 0 0 r{rnum}')
    elif command[0] == 'OP_ADD':
        print('# add')
        print('pop 0 0 r0')
        print('pop 0 0 r1')
        print('add r1 r0 r1')
        print('push r1 0 0')
    elif command[0] == 'OP_SUB':
        print('# sub')
        print('pop 0 0 r0')
        print('pop 0 0 r1')
        print('sub r1 r0 r1')
        print('push r1 0 0')
    elif command[0] == 'OP_NOP':
        print('# nop')
        print('addi 0 r0 r0')
    elif command[0] == '.label':
        print(' '.join(command)[1:])
    elif command[0] == 'OP_JMP':
        print('# jmp')
        print(f'mov {command[1]} 0 cnt')
    elif command[0] == 'OP_JEQ':
        print('# jeq')
        print('pop 0 0 r0')
        print('pop 0 0 r1')
        print(f'jeq r1 r0 {command[1]}')
    elif command[0] == 'OP_JGE':
        print('# jge')
        print('pop 0 0 r0')
        print('pop 0 0 r1')
        print(f'jge r1 r0 {command[1]}')
    elif command[0] == 'OP_CALL':
        print('# call')
        print(f'mov {command[1]} 0 cnt')
    elif command[0] == 'OP_SWAP':
        # stackの1番上と2番目を入れ替える
        print('# swap')
        print('pop 0 0 r0')
        print('pop 0 0 r1')
        print('push r0 0 0')
        print('push r1 0 0')
    elif command[0] == 'OP_RET':
        print('# ret')
        print('pop 0 0 cnt')
    elif command[0] == 'OP_STORE':
        print('# store')
        print('pop 0 0 r0')
        print('store r0 0 0')
    elif command[0] == 'OP_LOAD':
        print('# load')
        print('load 0 0 r0')
        print('push r0 0 0')
    else:
        print('unumplemented!', command)
    
