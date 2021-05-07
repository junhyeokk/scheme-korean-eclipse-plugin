import argparse
from boilerplate import *

QUOTE = 'QUOTE'
IF = 'IF'
CAR = 'CAR'
CDR = 'CDR'
CONS = 'CONS'
if korean:
    QUOTE = 'ㅇ'
    IF = 'ㄷ'
    CAR = 'ㅓ'
    CDR = 'ㅏ'
    CONS = 'ㅐ'


class Bindings:
    def __init__(self, parent):
        self.parent = parent
        self.symbols = dict()

    def add_symbol(self, symbol, value):
        if symbol.type == Type.SYM:
            self.symbols[symbol.value.upper()] = value

    def __str__(self):
        if isNil(self.parent):
            return f"ENV class : root"
        else:
            return f"ENV class : {str(self.parent)}"

    def __repr__(self):
        return self.__str__()

def env_create(parent):
    new_bindings = Bindings(parent)
    # if not isNil(parent):
    #     parent.add_child(new_bindings)
    return new_bindings

def env_get(env, symbol):
    parent = env.parent

    if symbol.value.upper() in env.symbols:
        return env.symbols[symbol.value.upper()]

    if type(parent) is Bindings:
        pass
    elif isNil(parent):
        # return "Error unbound", nilp()
        return nilp()

    return env_get(parent, symbol)

def env_set(env, symbol, value):
    env.add_symbol(symbol, value)
    # return ErrorType.ERROR_OK
    return "Error OK", nilp()

def listp(expr):
    while not isNil(expr):
        if expr.type != Type.PAIR:
            return False
        expr = expr.cdr()
    return True

def eval_expr(expr, env):
    if expr.type == Type.SYM:
        # return ErrorType.ERROR_OK, env_get(env, expr)
        return "Error OK", env_get(env, expr)
    elif expr.type != Type.PAIR:
        # return ErrorType.ERROR_OK, expr
        return "Error OK", expr

    if not listp(expr):
        # return ErrorType.ERROR_SYNTAX, nilp()
        return "Error Syntax", nilp()

    op = expr.car()
    args = expr.cdr()

    if op.type == Type.SYM:
        if op.value.upper() == QUOTE:     # 한글변환 'ㅇ', "QUOTE"
            if isNil(args) or not isNil(args.cdr()):
                return "Error Args", nilp()
            return "Error OK", args.car()
        elif op.value.upper() == "DEF":
            if isNil(args) or isNil(args.cdr()) or not isNil(args.cdr().cdr()):
                return "Error Args", nilp()
            sym = args.car()
            if sym.type != Type.SYM:
                return "Error Type", nilp()
            err, val = eval_expr(args.cdr().car(), env)

            env_set(env, sym, val)
            return "Error OK", sym
        elif op.value.upper() == "LAM": # lambda
            if isNil(args) or isNil(args.cdr()):
                return "Error Args", nilp()

            return make_closure(env, args.car(), args.cdr())
        elif op.value.upper() == IF:      # 한글변환 'ㄷ', "IF"
            if isNil(args) or isNil(args.cdr()) or isNil(args.cdr().cdr()) or not isNil(args.cdr().cdr().cdr()):
                return "Error Args", nilp()

            err, cond = eval_expr(args.car(), env)
            if err != "Error OK":
                return err, nilp()
            val = args.cdr().cdr().car() if isNil(cond) else args.cdr().car()
            return eval_expr(val, env)
    err, op = eval_expr(op, env)
    if err != "Error OK":
        return err, nilp()
    args = copy_list(args)
    p = args
    while not isNil(p):
        err, p.value[0] = eval_expr(p.car(), env)
        if err != "Error OK":
            return err, nilp()
        p = p.cdr()
    return apply(op, args)

    # return "Error Syntax", nilp()

def make_builtin(fn):
    a = Data()
    a.type = Type.BUILTIN
    a.value = fn
    return a

def make_closure(env, args, body):
    if not listp(args) or not listp(body):
        return "Error Syntax", nilp()

    p = args
    while not isNil(p):
        if p.car().type != Type.SYM:
            return "Error Type", nilp()
        p = p.cdr()

    result = cons(env, cons(args, body))
    result.type = Type.CLOSURE

    return "Error OK", result

def copy_list(lst):
    if isNil(lst):
        return nilp()

    a = cons(lst.car(), nilp())
    p = a
    lst = lst.cdr()

    while not isNil(lst):
        p.value[1] = cons(lst.car(), nilp())
        p = p.cdr()
        lst = lst.cdr()

    return a

def apply(fn, args):
    if fn.type == Type.BUILTIN:
        return fn.value(args)
    elif fn.type != Type.CLOSURE:
        return "Error Type", nilp()

    env = env_create(fn.car())
    arg_names = fn.cdr().car()
    body = fn.cdr().cdr()

    while not isNil(arg_names):
        if isNil(args):
            return "Error Args", nilp()
        env_set(env, arg_names.car(), args.car())
        arg_names = arg_names.cdr()
        args = args.cdr()

    if not isNil(args):
        return "Error Args", nilp()

    while not isNil(body):
        err, result = eval_expr(body.car(), env)
        if err != "Error OK":
            return err, nilp()
        body = body.cdr()

    return "Error OK", result

def builtin_car(args):
    return "Error OK", args.car().car()
    # if isNil(args) or not isNil(args.cdr()):
    #     return "Error Args", nilp()
    
    # if isNil(args.car()):
    #     return "Error OK", nilp()
    # elif args.car().type != Type.PAIR:
    #     return "Error Type", nilp()
    # else:
    #     return "Error OK", args.car().car()

def builtin_cdr(args):
    return "Error OK", args.car().cdr()
    # if isNil(args) or not isNil(args.cdr):
    #     return "Error Args", nilp()
    
    # if isNil(args.car()):
    #     return "Error OK", nilp()
    # elif args.car().type != Type.PAIR:
    #     return "Error Type", nilp()
    # else:
    #     return "Error OK", args.car().cdr()

def builtin_cons(args):
    if isNil(args) or isNil(args.cdr()) or not isNil(args.cdr().cdr()):
        return "Error Args", nilp()
    return "Error OK", cons(args.car(), args.cdr())

def builtin_add(args):
    if isNil(args) or isNil(args.cdr()) or not isNil(args.cdr().cdr()):
        return "Error Args", nilp()
    a = args.car()
    b = args.cdr().car()
    if a.type != Type.INT or b.type != Type.INT:
        return "Error Type", nilp()

    return "Error OK", mkint(args.car().value + args.cdr().car().value)

def builtin_subtract(args):
    if isNil(args) or isNil(args.cdr()) or not isNil(args.cdr().cdr()):
        return "Error Args", nilp()
    a = args.car()
    b = args.cdr().car()
    if a.type != Type.INT or b.type != Type.INT:
        return "Error Type", nilp()

    return "Error OK", mkint(args.car().value - args.cdr().car().value)

def builtin_multiply(args):
    if isNil(args) or isNil(args.cdr()) or not isNil(args.cdr().cdr()):
        return "Error Args", nilp()
    a = args.car()
    b = args.cdr().car()
    if a.type != Type.INT or b.type != Type.INT:
        return "Error Type", nilp()

    return "Error OK", mkint(args.car().value * args.cdr().car().value)

def builtin_divide(args):
    if isNil(args) or isNil(args.cdr()) or not isNil(args.cdr().cdr()):
        return "Error Args", nilp()
    a = args.car()
    b = args.cdr().car()
    if a.type != Type.INT or b.type != Type.INT:
        return "Error Type", nilp()

    return "Error OK", mkint(args.car().value // args.cdr().car().value)

def builtin_numeq(args):
    if isNil(args) or isNil(args.cdr()) or not isNil(args.cdr().cdr()):
        return "Error Args", nilp()
    a = args.car()
    b = args.cdr().car()
    if a.type != Type.INT or b.type != Type.INT:
        return "Error Type", nilp()

    result = mksym("T") if a.value == b.value else nilp()
    return "Error OK", result

def builtin_less(args):
    if isNil(args) or isNil(args.cdr()) or not isNil(args.cdr().cdr()):
        return "Error Args", nilp()
    a = args.car()
    b = args.cdr().car()
    if a.type != Type.INT or b.type != Type.INT:
        return "Error Type", nilp()

    result = mksym("T") if a.value < b.value else nilp()
    return "Error OK", result

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--codes')
    args = p.parse_args()

    env = env_create(nilp())

    env_set(env, mksym(CAR), make_builtin(builtin_car))       # 한글변환 'ㅓ', "CAR"
    env_set(env, mksym(CDR), make_builtin(builtin_cdr))       # 한글변환 'ㅏ', "CDR"
    env_set(env, mksym(CONS), make_builtin(builtin_cons))     # 한글변환 'ㅐ', "CONS"
    env_set(env, mksym("+"), make_builtin(builtin_add))
    env_set(env, mksym("-"), make_builtin(builtin_subtract))
    env_set(env, mksym("*"), make_builtin(builtin_multiply))
    env_set(env, mksym("/"), make_builtin(builtin_divide))
    env_set(env, mksym("T"), mksym("T"))
    env_set(env, mksym("="), make_builtin(builtin_numeq))
    env_set(env, mksym("<"), make_builtin(builtin_less))

    # while True:
    #     input_str = input(">> ")
    #
    #     while True:
    #         try:
    #             parsedlist = Parser(Lexer(input_str).lex())
    #             err, result = eval_expr(parsedlist, env)
    #             if err != "Error OK":
    #                 print(err)
    #             else:
    #                 print(result)
    #             break
    #         except IndexError:
    #             tmp = input("...  ")
    #             if tmp == '':
    #                 break
    #             input_str += tmp

    input_str = ""
    output_str = ""
    # print("한글ㅁㅁㅁ")
    # print(args.codes)
    new_line_keyword = "-*-*-"
    for code in args.codes.split(new_line_keyword):
        if code[0] == ';':
            continue
        input_str += code

        try:
            parsedlist = Parser(Lexer(input_str).lex())
        except:
            continue

        err, result = eval_expr(parsedlist, env)
        if err != "Error OK":
            output_str += err + new_line_keyword
            break
        else:
            output_str += str(result) + new_line_keyword
        input_str = ''

    print(output_str)