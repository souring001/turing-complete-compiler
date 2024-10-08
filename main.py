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

fib = """
r7 = fib(2)
def fib(r2):
    if r2 != 0:
        if r2 != 1:
            return fib(r2 - 1) + fib(r2 - 2)
    return 1
"""

read32 = """
r5 = 0
while(r5 != 32):
    RAM[r5] = r7
    r5 = r5 + 1
"""

test_r = """
r5 = r5 - 1
"""

sort_py = """
r5 = 0
while(r5 != 15):
    RAM[r5] = r7
    r5 = r5 + 1

r4 = 14
while(r4 != 0):
    r5 = 0
    while(r5 < r4):
        r2 = RAM[r5]
        r5 = r5 + 1
        r3 = RAM[r5]
        if r3 < r2:
            RAM[r5] = r2
            r5 = r5 - 1
            RAM[r5] = r3
            r5 = r5 + 1
    r4 = r4 - 1

r5 = 0
while(r5 != 15):
    r7 = RAM[r5]
    r5 = r5 + 1
"""

fruit_py = """
r7 = 0
r7 = 1
r7 = 0
r7 = 1
r7 = 1
r7 = 1
r7 = 0
r7 = 1
r7 = 2
r7 = 1
r7 = 1
r5 = 0
r2 = 0
r3 = 92
while(r2 != 1):
    while(r3 == 92):
        r3 = r7
        r7 = 3
    r5 = r3
    r3 = 92
    r4 = RAM[r5]
    if r4 == 1:
        r2 = 1
    else:
        RAM[r5] = 1
r7 = 2
r7 = 4
"""

planet_py = """
r3 = 1
while(0 != 1):
    r2 = r7
    if r3 == 1:
        r2 = r2 - 32
        r7 = r2
        r3 = 0
    else:
        r7 = r2
    if r2 == 32:
        r3 = 1

"""

maze_py = """
maze(0, -1, 3)

def maze(r2, r3, r4):
    if r4 == 0:
        return

    r2 = r2 + r3
    maze(r2, -r3, r4-1)
    r7 = r2

    r2 = r2 - r3
    maze(r2, r3, r4-1)
    r7 = r2
    maze(r2, r3, r4-1)

    r2 = r2 - r3
    maze(r2, -r3, r4-1)
    r7 = r2
"""

dance_py = """
r3 = r7
while(0 == 0):
    r4 = r3 ^ (r3 >> 1)
    r5 = r4 ^ (r4 + r4)
    r3 = r5 ^ (r5 >> 2)
    r7 = r3 & 0b11
"""

alloy_py = """
r2 = r7
r3 = r7
r4 = r7
r5 = r7
move(r2, r3, r4, r5)
def move(r2, r3, r4, r5):
    if r2 == 0:
        r7 = r3
        r7 = 5
        r7 = r4
        r7 = 5
    else:
        move(r2 - 1, r3, r5, r4)
        r7 = r3
        r7 = 5
        r7 = r4
        r7 = 5
        move(r2 - 1, r5, r4, r3)
    return 100
"""
# メモリ
# 0 : 0
# 1-16: 高さ
# 17: 0
# 33-48 (1-16 + 32): 左に存在する壁の高さ情報
# 65-80 (1-16 + 64): 右に存在する壁の高さ情報

# レジスタ
# r2: 合計水量
# r5: RAM

# 方針
# 1. 地面1〜16(i)でループ
#      高さをメモリに読み込む
#      左に存在する壁の高さを保持：max(高さ[i-1], 左壁の高さ[i-1])
# 2. 地面16〜1(i)でループ
#      右に存在する壁の高さを保持：max(高さ[i+1], 右壁の高さ[i+1])
#      水量を計算：min(左壁の高さ[i], 右壁の高さ[i]) - 高さ[i]
#      水量が正ならば合計水量に加算
# 3. 合計水量を出力

water_py = """
r5 = 1
r3 = 0
while(r5 < 17):
    RAM[r5] = r7
    r5 = r5 - 1
    if r3 < RAM[r5]:
        r3 = RAM[r5]
    r5 = r5 + 33
    RAM[r5] = r3
    r5 = r5 - 31

r3 = 0
while(0 < r5):
    # RAM[r5 + 64] = max(RAM[r5 + 1], RAM[r5 + 1 + 64])
    r5 = r5 + 1
    if r3 < RAM[r5]:
        r3 = RAM[r5]
    r5 = r5 + 63
    RAM[r5] = r3 # 右壁の高さ[i]

    # min(左壁の高さ[i], 右壁の高さ[i]) - 高さ[i]
    r5 = r5 - 32 # i + 32
    if r3 < RAM[r5]:
        r4 = r3
    else:
        r4 = RAM[r5]
    r5 = r5 - 32 # i
    if RAM[r5] < r4:
        r4 = r4 - RAM[r5]
        r2 = r2 + r4
    r5 = r5 - 1 # i--

# 合計水量を出力
r7 = r2
"""

exp = ast.parse(water_py, mode="exec")

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
    
    def visit_BitXor(self, node: ast.BitXor) -> ast.BitXor:
        print("OP_XOR")
        return node
    
    def visit_RShift(self, node: ast.RShift) -> ast.RShift:
        print("OP_SHR")
        return node
    
    def visit_Constant(self, node: ast.Constant) -> ast.Constant:
        print("OP_PUSH " + str(node.value))
        return node
    
    def visit_Name(self, node: ast.Name) -> ast.Name:
        if node.id not in ["r2", "r3", "r4", "r5", "r7"]:
            print("UNSUPPORTED Name")
        print("OP_PUSH" + node.id[-1])
        return node
    
    def visit_Subscript(self, node: ast.Subscript) -> ast.Subscript:
        if not isinstance(node.value, ast.Name):
                print("UNSUPPORTED Assign 4")
        if node.value.id != "RAM":
                print("UNSUPPORTED Assign 5")
        if not isinstance(node.slice, ast.Name):
                print("UNSUPPORTED Assign 6")
        if node.slice.id != "r5":
                print("UNSUPPORTED Assign 7")
        print("OP_LOAD")
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
                print("OP_JEQ ", end="")
            elif len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.Lt):
                self.visit(node.test.left)
                self.visit(node.test.comparators[0])
                print("OP_JGE ", end="")
            elif len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.Eq):
                self.visit(node.test.left)
                self.visit(node.test.comparators[0])
                print("OP_JNE ", end="")
            elif len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.GtE):
                self.visit(node.test.left)
                self.visit(node.test.comparators[0])
                print("OP_JLT ", end="")
        else:
            print("UNSUPPORTED IF")
        print(elselabel) # jump label
        for stmt in node.body:
            self.visit(stmt)
        print("OP_JMP " + endlabel)
        print(".label " + elselabel)
        if len(node.orelse) > 0:
            for stmt in node.orelse:
                self.visit(stmt)
        print(".label " + endlabel)
        return node

    def visit_While(self, node: ast.While) -> ast.While:
        if len(node.orelse) > 0:
            print("UNSUPPORTED While 1")
        startlabel = ".L" + str(self.label)
        self.label += 1
        endlabel = ".L" + str(self.label)
        self.label += 1
        print(".label " + startlabel)
        if isinstance(node.test, ast.Compare):
            if len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.NotEq):
                self.visit(node.test.left)
                self.visit(node.test.comparators[0])
                print("OP_JEQ ", end="")
            elif len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.Lt):
                self.visit(node.test.left)
                self.visit(node.test.comparators[0])
                print("OP_JGE ", end="")
            elif len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.Eq):
                self.visit(node.test.left)
                self.visit(node.test.comparators[0])
                print("OP_JNE ", end="")
        else:
            print("UNSUPPORTED While 2")
        print(endlabel) # jump label
        for stmt in node.body:
            self.visit(stmt)
        print("OP_JMP " + startlabel)
        print(".label " + endlabel)
        return node
    
    def visit_Call(self, node: ast.Call) -> ast.Call:
        if not isinstance(node.func, ast.Name):
            print("UNSUPPORTED Call")
        
        returnlabel = ".L" + str(self.label)
        self.label += 1
        print("OP_PUSH2")
        print("OP_PUSH3")
        print("OP_PUSH4")
        print("OP_PUSH5")
        print("OP_PUSH " + returnlabel)
        for arg in node.args:
               self.visit(arg)
        name = node.func.id
        print("OP_CALL .L_" + name)
        print(".label " + returnlabel)
        # calling convention
        print("OP_POP1")
        print("OP_POP5")
        print("OP_POP4")
        print("OP_POP3")
        print("OP_POP2")
        print("OP_PUSH1")
        return node
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        print(".label .L_"+node.name)
        rsize = len(node.args.args) + 1
        for i, arg in enumerate(node.args.args):
            if arg.arg != "r" + str(i + 2):
                print("UNSUPPORTED Arguments: should be r" + str(i + 2))
            print("OP_POP"+str(rsize - i))

        for stmt in node.body:
            self.visit(stmt)
        return node
    
    def visit_Return(self, node: ast.Return) -> ast.Return:
        if node.value != None:
            self.visit(node.value)
        else:
            print("OP_PUSH 0") # dummy
        print("OP_SWAP")
        print("OP_RET")
        return node
    
    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        if len(node.targets) > 1:
            print("UNSUPPORTED Assign 1")
        target = node.targets[0]
        if isinstance(target, ast.Name):
            if target.id not in ["r2", "r3", "r4", "r5", "r7"]:
                print("UNSUPPORTED Assign 2")
            self.visit(node.value)
            print("OP_POP" + target.id[-1])
        elif isinstance(target, ast.Subscript):
            if not isinstance(target.value, ast.Name):
                print("UNSUPPORTED Assign 4")
            if target.value.id != "RAM":
                print("UNSUPPORTED Assign 5")
            if not isinstance(target.slice, ast.Name):
                print("UNSUPPORTED Assign 6")
            if target.slice.id != "r5":
                print("UNSUPPORTED Assign 7")
            self.visit(node.value)
            print("OP_STORE")
        else:
            print("UNSUPPOPRTED Assign 3")
        return node
    
    def visit_Pass(self, node: ast.Pass) -> ast.Pass:
        print("OP_NOP")
        return node
PrintNodeVisitor().visit(exp)

