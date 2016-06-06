import ast
import operator as op
import math

## 출처: https://github.com/xdoju/Delphox/blob/master/arith.py
## 결과 formatting해서 리턴하는 calculate() 추가

def calculate(expr):
    if not expr:
        return "계산할 수식을 넣어달라냥! '/계산 1+1' 처럼 해주면 된다냥!"
    try:
        return str(eval_expr(expr))
    except SyntaxError:
        return "잘못된 수식이다냥!"
    except ValueError:
        return "히잉.. 너무 큰 숫자가 나와버렸다냥8ㅅ8"
    except:
        return "냐옹!?"


def power(a, b):
    if abs(b) > 1000:
        raise ValueError
    return a ** b

def divide(a, b):
    return float(a) / b

def fac(a):
    if a > 100:
        raise ValueError
    return math.factorial(a)

operators = {
    ast.Add : op.add,
    ast.Sub : op.sub,
    ast.Mult : op.mul,
    ast.Div : divide,
    ast.Mod : op.mod,
    ast.Pow : power,
    ast.LShift : op.lshift,
    ast.RShift : op.rshift,
    ast.BitOr : op.or_,
    ast.BitXor : op.xor,
    ast.BitAnd : op.and_,
    ast.FloorDiv : divide,
    ast.Invert : op.invert,
    ast.Not : op.not_,
    ast.UAdd : op.pos,
    ast.USub : op.neg
}

funcs = {
    'sin' : math.sin,
    'cos' : math.cos,
    'tan' : math.tan,
    'fac' : fac
}

def eval_expr(expr):
    if len(expr) > 80:
        raise SyntaxError
    return eval_(ast.parse(expr, mode='eval').body)

def eval_(node):
    v = 0
    if isinstance(node, ast.Num):
        v = node.n
    elif isinstance(node, ast.BinOp):
        v = operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp):
        v = operators[type(node.op)](eval_(node.operand))
    elif isinstance(node, ast.Name):
        if node.id == 'pi':
            v = math.pi
        elif node.id == 'e':
            v = math.e
        else:
            raise SyntaxError
    elif isinstance(node, ast.Call):
        funcname = node.func.id
        if len(node.args) > 1:
            raise SyntaxError
        v = funcs[funcname](eval_(node.args[0]))
    else:
        raise SyntaxError
    
    if len(str(v)) > 80:
        raise ValueError
    
    return v
