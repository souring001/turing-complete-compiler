file_name = 'fib.asm'

with open(file_name, 'r') as file:
    commands = [line.strip().split() for line in file]

print(commands)
