import sys

commands = [line.strip().split() for line in sys.stdin]

# file_name = 'asm_leg.asm'
# with open(file_name, 'r') as file:
#     commands = [line.strip().split() for line in file]

def comment_filter(commands):
    new_commands = []

    for command in commands:
        if command[0] == '#':
            continue
        new_commands.append(command)
    
    return new_commands    

def push_pop_filter(commands):
    new_commands = []

    i = 0
    while i < len(commands):
        command = commands[i]
        
        if i == len(commands) - 1:
            new_commands.append(command)
            break
        
        opecode = command[0]
        if opecode == 'push':
            next_opecode = commands[i+1][0]
            if next_opecode == 'pop':
                new_commands.append(['addi', '0', command[1], commands[i+1][3]])
                i += 2
                continue
        
        new_commands.append(command)
        i += 1
    return new_commands

def nop_filter(commands):
    new_commands = []

    for command in commands:
        if command[0] == 'addi' and command[2] == command[3]:
            continue
        new_commands.append(command)
    
    return new_commands

def dst_match_addi_filter(commands):
    # mov 0 0 r0
    # addi 0 r0 r4
    # ->
    # mov 0 0 r4
    new_commands = []

    i = 0
    while i < len(commands):
        command = commands[i]
        
        if i == len(commands) - 1:
            new_commands.append(command)
            break
        
        opecode = command[0]
        if opecode in ['add', 'addi', 'sub', 'subi2', 'and', 'load', 'pop', 'mov']:
            next_command = commands[i+1]
            if next_command[0] == 'addi' and next_command[1] == '0' and command[3] == next_command[2]:
                new_commands.append([opecode, command[1], command[2], next_command[3]])
                i += 2
                continue
        
        new_commands.append(command)
        i += 1
    return new_commands

def src_match_addi_filter(commands):
    # addi 0 r3 r0
    # store r0 0 0
    # ->
    # store r3 0 0
    new_commands = []

    i = 0
    while i < len(commands):
        command = commands[i]
        
        if i == len(commands) - 1:
            new_commands.append(command)
            break
        
        opecode = command[0]
        if opecode == 'addi':
            next_command = commands[i+1]
            if next_command[0] in ['add', 'addi', 'sub', 'subi2', 'and', 'store', 'push', 'jeq', 'jge'] and (next_command[1] == command[3] or next_command[2] == command[3]):
                src1 = next_command[1]
                src2 = next_command[2]
                if next_command[1] == command[3]:
                    src1 = command[2]
                if next_command[2] == command[3]:
                    src2 = command[2]
                new_commands.append([next_command[0], src1, src2, next_command[3]])
                i += 2
                continue
        
        new_commands.append(command)
        i += 1
    return new_commands

def push_mov_filter(commands):
    # push r4 0 0
    # mov 1 0 r0
    # ->
    # mov 1 0 r0
    # push r4 0 0
    new_commands = []

    i = 0
    while i < len(commands):
        command = commands[i]
        
        if i == len(commands) - 1:
            new_commands.append(command)
            break
        
        opecode = command[0]
        if opecode in ['push']:
            next_command = commands[i+1]
            if next_command[0] == 'mov' and next_command[3] != command[1] and (command[1] != 'cnt' or next_command[3] != 'cnt'):
                new_commands.append(next_command)
                new_commands.append(command)
                i += 2
                continue
        
        new_commands.append(command)
        i += 1
    return new_commands


def lists_match(l1, l2):
    if len(l1) != len(l2):
        return False
    return all(x == y and type(x) == type(y) for x, y in zip(l1, l2))

def match_commands(old_commands, new_commands):
    if len(old_commands) != len(new_commands):
        return False
    
    for x, y in zip(old_commands, new_commands):
        return lists_match(x, y)

filters = [push_pop_filter, nop_filter, dst_match_addi_filter, push_mov_filter, src_match_addi_filter]
# filters = [push_pop_filter, nop_filter, dst_match_addi_filter]

old_commands = comment_filter(commands)
new_commands = []
while True:
    new_commands = old_commands
    for filter in filters:
        new_commands = filter(new_commands)

    if match_commands(old_commands, new_commands):
        break

    old_commands = new_commands

for c in new_commands:
    print(' '.join(c))