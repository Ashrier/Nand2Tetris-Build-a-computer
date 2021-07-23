import sys

class Parser:
    def __init__(self, inst):
        self.inst = inst
        self.type = None
        self.valueX = None
        self.DestX=None
        self.CompX=None
        self.JumpX = None
        self.CleanUp()
        self.InstType()

    def InstType(self):
        #This function will tell get rid of comments so that we do not convert
        #them to binary, and it will tell us if the instructions is an A or C instructions

        if self.inst == '':
            return
        elif self.inst.startswith('@'):
            self.type = 'A'
        elif self.inst.startswith('('):
            self.type = 'L'
        else:
            self.type = "C"

    def value(self):
        if self.type != 'A':
            return None
        self.valueX = self.inst[1:].split()[0]
        return self.valueX

    def CleanUp(self):
        self.inst = self.inst.strip()
        cInside = self.inst.find('//')
        if cInside == -1:
            self.inst = self.inst.strip()
        elif cInside == 0:
            self.inst = ''
        else:
            self.inst = self.inst[0:cInside].strip()

    def Dest(self):
        eInside = self.inst.find('=')
        if self.type != 'C' or eInside == -1:
            return None
        self.DestX = self.inst[0:eInside].strip()
        return self.DestX

    def Comp(self):
        eInd = self.inst.find('=')
        sInd = self.inst.find(';')
        if self.type != 'C':
            return None
        if eInd != -1 and sInd != -1:
            self.CompX = self.inst[eInd+1:sInd].strip()
        elif eInd != -1 and sInd == -1:
            self.CompX = self.inst[eInd+1:].strip()
        elif eInd == -1 and sInd != -1:
            self.CompX = self.inst[0:sInd].strip()
        elif eInd == -1 and sInd == -1:
            self.CompX = self.inst.split()
        return self.CompX

    def Jump(self):
        sInd = self.inst.find(';')
        if self.type != 'C':
            return None
        if sInd != -1:
            self.JumpX = self.inst[sInd+1:].strip()
        return self.JumpX

class Code:
    def __init__(self, term):
        self.term = term
        self.valueB = None
        self.destB = None
        self.jumpB = None
        self.compB = None

    def decimalToBinary(self,n):
        return format(n, '016b')

    def value(self):
        if self.term == None:
            return None
        self.valueB = self.decimalToBinary(int(self.term))
        return self.valueB

    def Dest(self):
        if self.term == None:
            self.destB = '000'
        elif self.term == 'M':
            self.destB ='001'
        elif self.term == 'D':
            self.destB ='010'
        elif self.term == 'MD':
            self.destB ='011'
        elif self.term == 'A':
            self.destB ='100'
        elif self.term == 'AM':
            self.destB ='101'
        elif self.term == 'AD':
            self.destB ='110'
        elif self.term == 'AMD':
            self.destB ='111'
        return self.destB

    def Jump(self):
        if self.term == None:
            self.jumpB = '000'
        elif self.term == 'JGT':
            self.jumpB = '001'
        elif self.term == 'JEQ':
            self.jumpB = '010'
        elif self.term == 'JGE':
            self.jumpB = '011'
        elif self.term == 'JLT':
            self.jumpB = '100'
        elif self.term == 'JNE':
            self.jumpB = '101'
        elif self.term == 'JLE':
            self.jumpB = '110'
        elif self.term == 'JMP':
            self.jumpB = '111'
        return self.jumpB

    def Comp(self):
        if self.term == '0':
            self.compB = '0101010'
        elif self.term == '1':
            self.compB = '0111111'
        elif self.term == '-1':
            self.compB = '0111010'
        elif self.term == 'D':
            self.compB = '0001100'
        elif self.term == 'A':
            self.compB = '0110000'
        elif self.term == 'M':
            self.compB = '1110000'
        elif self.term == '!D':
            self.compB = '0001101'
        elif self.term == '!A':
            self.compB = '0110001'
        elif self.term == '!M':
            self.compB = '1110001'
        elif self.term == 'D+1':
            self.compB = '0011111'
        elif self.term == 'A+1':
            self.compB = '0110111'
        elif self.term == 'M+1':
            self.compB = '1110111'
        elif self.term == 'D-1':
            self.compB = '0001110'
        elif self.term == 'A-1':
            self.compB = '0110010'
        elif self.term == 'M-1':
            self.compB = '1110010'
        elif self.term == 'D+A':
            self.compB = '0000010'
        elif self.term == 'D+M':
            self.compB = '1000010'
        elif self.term == 'D-A':
            self.compB = '0010011'
        elif self.term == 'D-M':
            self.compB = '1010011'
        elif self.term == 'A-D':
            self.compB = '0000111'
        elif self.term == 'M-D':
            self.compB = '1000111'
        elif self.term == 'D&A':
            self.compB = '0000000'
        elif self.term == 'D&M':
            self.compB = '1000000'
        elif self.term == 'D|A':
            self.compB = '0010101'
        elif self.term == 'D|M':
            self.compB = '1010101'
        return self.compB

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.addPreDef()

    def addPreDef(self):
        for i in range(16):
            self.symbols['R'+str(i)] = i
        self.symbols['SCREEN']=16384
        self.symbols['KBD']=24576
        self.symbols['SP']=0
        self.symbols['LCL']=1
        self.symbols['ARG']=2
        self.symbols['THIS']=3
        self.symbols['THAT']=4

    def exists(self, symbol):
        if self.symbols.get(symbol) == None:
            return False
        else:
            return True

    def addSym(self, symbol, value):
        self.symbols[symbol] = value

    def getVal(self, symbol):
        return self.symbols.get(symbol)

class Passs:
    def __init__(self, symTab):
            self.symTab = symTab

    def firstPass(self):
        with open(sys.argv[1], 'r') as asm:
            lineNo = -1
            for inst in asm:
                p = Parser(inst)
                print(p.inst)
                if p.type == 'A' or p.type == 'C':
                    lineNo += 1
                if p.type == 'L':
                    symbol = p.inst[1:-1]
                    if not self.symTab.exists(symbol):
                        print(symbol)
                        self.symTab.addSym(symbol, lineNo+1)

    def secPass(self):
        with open(sys.argv[1].split('.')[0]+'.hack', 'a') as hack:
            with open(sys.argv[1], 'r') as asm:
                n = 16
                for inst in asm:
                    p = Parser(inst)
                    print(f'sec: {p.inst}')
                    if p.type == 'A':
                        symbol = p.inst[1:]
                        if self.symTab.exists(symbol):
                            c = Code(self.symTab.getVal(symbol))
                            hack.write(c.value()+'\n')
                            print(c.value())
                        else:
                            try:
                                val = int(symbol)
                                c = Code(val)
                                hack.write(c.value()+'\n')
                            except ValueError:
                                self.symTab.addSym(symbol, n)
                                c = Code(n)
                                hack.write(c.value()+ '\n')
                                n += 1
                    elif p.type == 'C':
                        d = Code(p.Dest())
                        c = Code(p.Comp())
                        j = Code(p.Jump())
                        hack.write('111'+c.Comp()+d.Dest()+j.Jump()+'\n')
                        print('111'+c.Comp()+d.Dest()+j.Jump())
                        print(f'Jump: {j.Jump()}')
                        print(f'Dest: {d.Dest()}')
                        print(f'Comp: {c.Comp()}')

def main():
    st = SymbolTable()
    print(st.symbols)
    pas = Passs(st)
    pas.firstPass()
    pas.secPass()
    print(st.symbols)
            #for line in asm:
                #p = Parser(inst)
                #if p.type == 'A':
                    #c = Code(p.value())
                    #hack.write(c.value()+'\n')
                    #print(c.value())
                #if p.type == 'C':
                    #d = Code(p.Dest())
                    #c = Code(p.Comp())
                    #j = Code(p.Jump())
                    #hack.write('111'+c.Comp()+d.Dest()+j.Jump()+'\n')
                    #print('111'+c.Comp()+d.Dest()+j.Jump())
                    #print(f'Jump: {j.Jump()}')
                    #print(f'Dest: {d.Dest()}')
                    #print(f'Comp: {c.Comp()}')
                #print(f'Jump: {p.Jump()}')
                #print(f'Dest: {p.Dest()}')
                #print(f'Comp: {p.Comp()}')
                #print(p.inst)

if __name__ == '__main__':
    main()
