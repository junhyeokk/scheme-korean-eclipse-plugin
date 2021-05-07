from enum import Enum

korean = True
LAMBDA = 'lambda'
DEFINE = 'define'
if korean:
    LAMBDA = 'ㅅ'
    DEFINE = 'ㅋ'

class Type(Enum):
    NIL = 0
    INT = 1
    REAL = -2
    SYM = -1
    PAIR = 2
    BUILTIN = 3
    CLOSURE = 4

class ErrorType(Enum):
    UNEXPECTED_TOKEN = 'Unexpected Token'
    ID_INVALID_TOKEN = 'invaild type'
    NO_INPUT_FILE = 'No Input File'
    ERROR_SYNTAX = 'Error Syntax'
    ERROR_OK = 0

class Error(Exception):
    pass

def Err(token, type):
    raise Error("{0} : {1}".format(
        str(type), str(token)
    ))

class Token(object):
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def __str__(self):
        return self.__class__.__name__ + "(" + \
               str(self.value) + ")" + "." + str(self.type)

    def __repr__(self):
        return self.__str__()

class Input:
    def __init__(self):
        self.text = ""

    def _input(self):
        self.text = input(">> ")
        if self.text == "exit":
            exit()
        return self.text

class Keyword(Enum):
    LPAREN = 4
    RPAREN = 5
    DEFINE = 6
    LAMBDA = 7
    PLUS_OP = 8
    SUB_OP = 9
    DIV_OP = 10
    MUL_OP = 11
    DEF = 12
    QUOTE = 13
    EQ = 14
    LESS = 15

class Data:
    def __init__(self, type=Type.NIL, value=0):
        self.type = type
        self.value = value

    def car(self):
        return self.value[0]

    def cdr(self):
        return self.value[1]

    def __str__(self):
        if self.type == Type.NIL:
            return "NIL"
        elif self.type == Type.PAIR:
            try:
                if (self.cdr() == int(self.cdr())):
                    return "(" + str(self.car()) + " . " + str(self.cdr()) + ")"
            except:
                retStr = '('
                retStr += str(self.car())
                atom = self.cdr()
                while (atom.type != Type.NIL):
                    if (atom.type == Type.PAIR):
                        retStr += ' . '
                        retStr += str(atom.car())
                        atom = atom.cdr()
                    elif (atom.type == Type.BUILTIN):
                        retStr += ' . '
                        retStr += "Builtin" + str(atom.value)
                    else:
                        retStr += ' . '
                        retStr += str(atom)
                        break
                retStr += ')'
                return str(retStr)
        else:
            return str(self.value)

    def __repr__(self):
        return self.__str__()

class Nil:
    pass

def cons(a, b):
    return Token(Type.PAIR, (a, b))

class Lit:      # Literal?
    def __init__(self, value, type):
        self.value = int(token.value) if value.type == Type.INT else float(token.value)
        self.type = str(token.type)

class Symbol:
    def __init__(self, value, type):
        self.value = str(value.value)
        self.type = str(value.type)

class Pair:
    def __init__(self, root=None, LV=None, RV=None):
        self.root = root
        self.LV = LV
        self.RV = RV

def isNil(d):
    return d.type == Type.NIL

def nilp():
    return Data(Type.NIL)

def cons(d1, d2):
    return Data(Type.PAIR, [d1, d2])

def mkint(n):
    return Data(Type.INT, n)

def mksym(s):
    return Data(Type.SYM, s)

class Lexer:
    def __init__(self, text):
        self.pos = 0
        self.text = text if len(text) != 0 else Err(Type.NIL, ErrorType.NO_INPUT_FILE)
        self.currentToken = self.text[self.pos]

    def eat(self, tokenType):
        if self.currentToken == tokenType:
            return True
        return False

    def jmp(self):
        if self.pos == len(self.text) - 1:
            self.currentToken = None
            return False
        else:
            self.pos += 1
            self.currentToken = self.text[self.pos]
            return True

    def lex(self):
        lexR = []
        # print("===== === LEX === =====")
        while True:
            if self.pos == len(self.text) or self.currentToken == None:
                break

            if self.currentToken.isspace():
                try:
                    while self.currentToken.isspace():
                        self.jmp()
                except:
                    break

            elif self.currentToken == ".":
                self.jmp()

            elif self.currentToken == "(":
                if not self.eat("("):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("(", Keyword.LPAREN))
                self.jmp()
                if self.currentToken == ")":
                    lexR.append(Token(")", Keyword.RPAREN))
                    self.jmp()

            elif self.currentToken == ")":
                if not self.eat(")"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token(")", Keyword.RPAREN))
                self.jmp()

            elif self.currentToken.isalpha():
                id = ""
                while self.currentToken.isalpha() and self.currentToken is not None:
                    if self.currentToken.isalpha():
                        id += self.currentToken
                        if (self.jmp()):
                            pass
                        else:
                            break
                if id == LAMBDA:      # 한글변환 'ㅅ', "lambda"
                    lexR.append(Token('LAM', Keyword.LAMBDA))
                elif id == DEFINE:    # 한글변환 'ㅋ', define"
                    lexR.append(Token('DEF', Keyword.DEF))
                elif id == "Nil":
                    lexR.append(Token('NIL', Type.NIL))
                else:
                    lexR.append(Token(id, Type.SYM))

            elif self.currentToken.isdigit():
                num = ""
                realFlag = False
                while self.currentToken.isdigit() or self.currentToken == ".":
                    if self.currentToken == ".":
                        realFlag = True
                        num += self.currentToken
                        if (self.jmp()):
                            pass
                        else:
                            break
                    else:
                        num += self.currentToken
                        if (self.jmp()):
                            pass
                        else:
                            break
                if realFlag:
                    lexR.append(Token(num, Type.REAL))
                else:
                    lexR.append(Token(num, Type.INT))

            elif self.currentToken == "+":
                if not self.eat("+"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("+", Keyword.PLUS_OP))
                self.jmp()

            elif self.currentToken == "-":
                if not self.eat("-"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("-", Keyword.SUB_OP))
                self.jmp()

            elif self.currentToken == "*":
                if not self.eat("*"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("*", Keyword.MUL_OP))
                self.jmp()

            elif self.currentToken == "/":
                if not self.eat("/"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("/", Keyword.DIV_OP))
                self.jmp()

            elif self.currentToken == "=":
                if not self.eat("="):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("=", Keyword.EQ))
                self.jmp()

            elif self.currentToken == "<":
                if not self.eat("<"):
                    return Err(self.currentToken, ErrorType.UNEXPECTED_TOKEN)
                lexR.append(Token("<", Keyword.LESS))
                self.jmp()

        # print(lexR)
        # print("===== === OUT === =====")
        return lexR

def iCons(d_list):
    if len(d_list) != 1:
        return cons(d_list[0], iCons(d_list[1:]))
    else:
        return cons(d_list[0], nilp())

def Parser(tokenlist):
    if len(tokenlist) == 0:
        return Err(Nil(), ErrorType.NO_INPUT_FILE)
    LA = tokenlist.pop(0)
    if LA.type == Keyword.LPAREN:
        if tokenlist[0].type == Keyword.RPAREN:
            return nilp()
        L = []
        while tokenlist[0].type != Keyword.RPAREN:
            L.append(Parser(tokenlist))
        tokenlist.pop(0)
        LR = iCons(L)
        return LR
    elif LA.type == Keyword.RPAREN:
        return Err(LA, ErrorType.UNEXPECTED_TOKEN)
    else:
        if LA.value.isdigit():      # int
            return Data(Type.INT, int(LA.value))
        elif LA.value.replace('.', '', 1).isdigit():        # float
            return Data(Type.REAL, float(LA.value))
        else:
            return Data(Type.SYM, str(LA.value))

if __name__ == "__main__":
    while True:
        parsedlist = Parser(Lexer(Input()._input()).lex())
        print("\n===== === PAR === =====")
        print(parsedlist)
        print("===== === OUT === =====")
