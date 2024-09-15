import ast

PMEM = []
STACK = []
ip = 0
sp = 0
REGS = [0] * 8

OP_NOP = 0x00
OP_ADD = 0x01
OP_SUB = 0x02
OP_AND = 0x08
OP_NOT = 0x09
OP_JEQ = 0x10 #1
OP_PUSH = 0x20 #1
OP_PUSH2 = 0x22
OP_PUSH3 = 0x23
OP_PUSH4 = 0x24
OP_PUSH5 = 0x25
OP_POP = 0x28
OP_POP2 = 0x29
OP_POP3 = 0x2a
OP_POP4 = 0x2b
OP_POP5 = 0x2c
OP_STORE = 0x30
OP_LOAD = 0x31
OP_DUP = 0x40
OP_IN = 0xf0
OP_OUT = 0xf1
OP_HLT = 0xFF

def push(n):
    global STACK
    STACK.append(n)

def pop():
    global STACK
    return STACK.pop()

PMEM = [
    OP_PUSH, 0x10,
    OP_PUSH, 0x21,
    OP_ADD,
    OP_DUP,
    OP_OUT,
    OP_PUSH, 0x1,
    OP_ADD,
    OP_OUT,
]

exp = ast.parse("""
def fib(r2):
    if r2 != 0:
        if r2 != 1:
            return fib(r2 - 1) + fib(r2 - 2)
    return 1
""", mode="exec")

class PrintNodeVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.label = 0
        super().__init__()

    def visit(self, node):
        # print(node)
        super().visit(node)
        return node
    
    def visit_Expr(self, node: ast.Expr) -> ast.Expr:
        self.visit(node.value)
        print("OP_POP")
        return node
    
    def visit_BinOp(self, node: ast.BinOp) -> ast.BinOp:
        self.visit(node.left)
        self.visit(node.right)
        super().visit(node.op)
        return node
    
    def visit_Add(self, node: ast.Add) -> ast.Add:
        print("OP_ADD")
        return node

    def visit_Sub(self, node: ast.Sub) -> ast.Sub:
        print("OP_SUB")
        return node
    
    def visit_BitAnd(self, node: ast.BitAnd) -> ast.BitAnd:
        print("OP_AND")
        return node
    
    def visit_Constant(self, node: ast.Constant) -> ast.Constant:
        print("OP_PUSH " + str(node.value))
        return node
    
    def visit_Name(self, node: ast.Name) -> ast.Name:
        if node.id not in ["r2", "r3", "r4", "r5"]:
            print("UNSUPPORTED Name")
        print("OP_PUSH" + node.id[-1])
        return node

    def visit_If(self, node: ast.If) -> ast.If:
        endlabel = ".L" + str(self.label)
        self.label += 1
        elselabel = ".L" + str(self.label)
        self.label += 1
        if isinstance(node.test, ast.Compare):
            if len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.NotEq):
                self.visit(node.test.left)
                self.visit(node.test.comparators[0])
                print("OP_JEQ")
        else:
            print("UNSUPPORTED IF")
        print(elselabel) # jump label
        for stmt in node.body:
            self.visit(stmt)
        print("OP_JMP " + endlabel)
        print(".label " + elselabel)
        if len(node.orelse) > 0:
            self.visit(node.orelse[0])
        print(".label " + endlabel)
        return node

    def visit_While(self, node: ast.While) -> ast.While:
        if len(node.orelse) > 0:
            print("UNSUPPORTED While 1")
        startlabel = ".L" + str(self.label)
        self.label += 1
        endlabel = ".L" + str(self.label)
        self.label += 1
        if isinstance(node.test, ast.Compare):
            if len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.NotEq):
                self.visit(node.test.left)
                self.visit(node.test.comparators[0])
                print("OP_JEQ")
        else:
            print("UNSUPPORTED While 2")
        print(endlabel) # jump label
        for stmt in node.body:
            self.visit(stmt)
        print("OP_JMP")
        print(startlabel)
        print(".label " +  endlabel)
        return node
    
    def visit_Call(self, node: ast.Call) -> ast.Call:
        if not isinstance(node.func, ast.Name):
            print("UNSUPPORTED Call")
        
        print("op_pusha")
        print("op_push_ret_addr")
        for arg in node.args:
               self.visit(arg)
        name = node.func.id
        print("OP_CALL")
        print(".L_"+name)
        print("op_save_top_to_r1")
        print("op_popa")
        print("op_push_r1")
        return node
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        print(".L_"+node.name)
        for i in range(len(node.args.args)):
            rsize = len(node.args.args) + 1
            print("OP_POP"+str(rsize - i))

        for stmt in node.body:
            self.visit(stmt)
        return node
    
    def visit_Return(self, node: ast.Return) -> ast.Return:
        if node.value != None:
            self.visit(node.value)
        else:
            print("OP_PUSH 0") # dummy
        print("OP_RET")
        return node
    
    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        if len(node.targets) > 1:
            print("UNSUPPORTED Assign 1")
        target = node.targets[0]
        if not isinstance(target, ast.Name):
            print("UNSUPPORTED Assign 2")
        if target.id not in ["r2", "r3", "r4", "r5"]:
            print("UNSUPPORTED Assign 3")
        self.visit(node.value)
        print("OP_POP" + target.id[-1])
        return node
PrintNodeVisitor().visit(exp)

while(ip < len(PMEM) and PMEM[ip] != OP_HLT):
    op = PMEM[ip]
    if op == OP_NOP:
        pass
    elif op == OP_ADD:
        op1 = pop()
        op2 = pop()
        push(op1 + op2)
    elif op == OP_SUB:
        op1 = pop()
        op2 = pop()
        push(op1 + op2)
    elif op == OP_AND:
        op1 = pop()
        op2 = pop()
        push(op1 & op2)
    elif op == OP_NOT:
        op1 = pop()
        push(~op1)
    elif op == OP_JEQ:
        op1 = pop()
        op2 = pop()
        ip += 1
        addr = PMEM[ip]
        if op1 == op2:
            ip = addr
            continue
    elif op == OP_PUSH:
        ip += 1
        op1 = PMEM[ip]
        push(op1)
    elif op == OP_PUSH2:
        push(REGS[2])
    elif op == OP_PUSH3:
        push(REGS[3])
    elif op == OP_PUSH4:
        push(REGS[4])
    elif op == OP_PUSH5:
        push(REGS[5])
    elif op == OP_POP:
        pop()
    elif op == OP_POP2:
        REGS[2] = pop()
    elif op == OP_POP3:
        REGS[3] = pop()
    elif op == OP_POP4:
        REGS[4] = pop()
    elif op == OP_POP5:
        REGS[5] = pop()
    elif op == OP_DUP:
        op1 = pop()
        push(op1)
        push(op1)
    elif op == OP_IN:
        op1 = input()
        op1 = int(op1) % 256
        push(op1)
    elif op == OP_OUT:
        op1 = pop()
        print(op1)
    else:
        print("unknown opcode" + str(op))
        exit()
    ip += 1

