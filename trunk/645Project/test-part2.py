import tkFileDialog

def extract(text, sub1, sub2):
    """
    extract a substring from text between first
    occurances of substrings sub1 and sub2
    """
    #Needs to be fixed
    temp = text.split(sub1, 1)[-1].split(sub2, 1)[0]
    temp = temp.strip()
    return temp.split("\n")

def storeInDict(text, dict):
    temp = []
    for line in text:
        line = line.strip()
        words = line.split('  ')
        key = words[0]
        value = words[1]
        dict[key] = int(value)
        temp.append(words)
    return temp

def LD(item, memory, regs):
    loop = 'loop:'
    for i in item:
        print i
        if i == 'LD':
            if item[0].lower() == loop:
                dest = item[2]
                source = item[3]
            else:
                dest = item[1]
                source = item[2]
            result = source.translate(None, ')').split('(')
            loc = int(result[0]) + regs[result[1]]
            memValue = memory[str(loc)]
            #memValue = memory[str(0)]
            regs[dest] = memValue    

def DADD(item, memory, regs):
    loop = 'loop:'
    for i in item:
        if i == 'DADD':
            if item[0].lower() == loop:
                dest = item[2]
                source1 = regs[item[3]]
                source2 = regs[item[4]]
            else:
                dest = item[1]
                source1 = regs[item[2]]
                source2 = regs[item[3]]
            #print source1, source2
            answer = source1 + source2
            #print answer
            regs[dest] = answer
            
def DADDI(item, memory, regs):
    loop = 'loop:'
    for i in item:
        if i == 'DADDI':
            if item[0].lower() == loop:
                dest = item[2]
                source1 = regs[item[3]]
                source2 = item[4]
            else:
                dest = item[1]
                source1 = regs[item[2]]
                source2 = item[3]
            source2 = source2.translate(None, '#')
            answer = source1 + int(source2)
            #print answer
            regs[dest] = answer

def SD(item, memory, regs):            
    loop = 'loop:'
    for i in item:    
        if i == 'SD':
            if item[0].lower() == loop:
                temp = item[2]
                addr = temp.translate(None, ')').split('(')
                dest = int(addr[0]) + regs[addr[1]]
                source = regs[item[3]]
                memory[dest] = source
            
            else:
                temp = item[1]
                addr = temp.translate(None, ')').split('(')
                dest = int(addr[0]) + regs[addr[1]]
                source = regs[item[2]]
                memory[dest] = source

def BNEZ(item, memory, regs):                
    for i in item:
        if i == "BNEZ":
            cmp = regs[item[1]]
            if cmp == 0:
                return False
            else:
                return True

def unroll(op, memory, regs):
    IO = []
    pc = 0
    spot = 0
    loop = 'loop:'
    index = 1
    numLoop = 0
    func = {'LD':LD, 'SD':SD, 'DADD':DADD, 'DADDI':DADDI, 'BNEZ':BNEZ}
    while index < (len(op)):
        for item in op:
            if item[0] == 'LD':
                if index > (len(op)):
                    break
                IO.append(op[index-1])
                LD(item, memory, regs)
                pc += 1
            if item[0] == 'SD':
                if index > (len(op)):
                    break
                IO.append(op[index-1])
                SD(item, memory, regs)
                pc += 1
            if item[0].lower() == loop:
                if index > (len(op)):
                    break
                IO.append(op[index-1])
                varstring = item[1]
                func[varstring](item, memory, regs)
                spot = pc
                pc += 1
            if item[0] == 'DADD':
                if index > (len(op)):
                    break
                IO.append(op[index-1])
                DADD(item, memory, regs)
                pc += 1
            if item[0] == 'DADDI':
                if index > (len(op)):
                    break
                IO.append(op[index-1])
                DADDI(item, memory, regs)
                pc += 1
            if item[0] == 'BNEZ':
                if index > (len(op)):
                    break
                IO.append(op[index-1])
                numLoop += 1
                temp = BNEZ(item, memory, regs)
                if temp == False:
                    """
                        last change is below-
                        delete pass and remove comment to revert
                    """
                    #index = pc
                    pass
                                
                if temp == True:
                    pc = spot
                    index = pc
            
            index += 1
    return (numLoop, IO)

def checkDepend(loopCount, op, instructions):
    temp = []
    check = ['0', '0']
    while loopCount != 0:
        for item in op:
            if item[0] == "Loop:":
                temp = item[1:]
                length = len(item) - 1
            else:
                temp = list(item)
                length = len(item)
        
            if check[1] == item[length-2] or check[1] == item[length - 1]:
                if item[0] == 'BNEZ':
                    currenti = ['IF1', 's', 's', 's', 'IF2', 'ID', 'EX', 'MEM1', 'MEM2', 'WB']
                    instructions.append(currenti)
                    if loopCount != 1:
                        currenti = ['IF1', 's', 's', 's', 's', 's', 's', 's', 's', 's']
                        instructions.append(currenti)
                else:
                    currenti = ['IF1', 's', 's', 's', 'IF2', 'ID', 'EX', 'MEM1', 'MEM2', 'WB']
                    instructions.append(currenti)
        #    elif item[0] == 'BNEZ':
        #         currenti = ['IF1', 's', 's', 's', 's', 's', 's', 's', 's', 's']
        #         instructions.append(currenti)
            else:
                currenti = ['IF1', 'IF2', 'ID', 'EX', 'MEM1', 'MEM2', 'WB']
                instructions.append(currenti)
    
            check = temp[:]
        loopCount -= 1
      
file = tkFileDialog.askopenfile(title="Open input data file",
                                mode='r',
                                filetypes=[("all formats", "*")])
regs = {}
for x in range(32):
    key = 'R' + str(x)
    regs[key] = 0

memory = {}
for x in range(0, 996, 8):
    memory[str(x)] = 0

text = file.read()
reg = extract(text, 'REGISTERS', 'MEMORY')
mem = extract(text, 'MEMORY', 'CODE')
code = extract(text, 'CODE', 'EOF')
 
reg = storeInDict(reg, regs)
mem = storeInDict(mem, memory)

op = []
for element in code:
    line = element.strip()
    newline = line.translate(None, ',')
    word = newline.split()
    op.append(word)

unroll = unroll(op, memory, regs)
numLoop = unroll[0]
IO = unroll[1]

depend = []
checkDepend(numLoop, IO, depend)
print depend

file.close()
"""
x=0
while x < 3:
    for op[x] in op:
        print op[x][0]
        x += 1
"""
"""
LD(['LD', 'R2', '0(R1)'], memory, regs)
DADD(['DADD', 'R4', 'R2', 'R3'], memory, regs)
SD(['SD', '0(R1)', 'R4'], memory, regs)
DADDI(['DADDI', 'R1', 'R1', '#-8'], memory, regs)
BNEZ(['BNEZ', 'R1', 'Loop'], memory, regs)
DADD(['DADD', 'R2', 'R2', 'R4'], memory, regs)
"""