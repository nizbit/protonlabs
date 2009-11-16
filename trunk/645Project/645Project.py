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

def process(op, memory, regs, loopCount):
    go = True
    loopCount = 0
    while go == True:
        for item in op:
            for i in item:
                if i == 'Loop:':
                    continue
                """
                Need to add checking if R0 is trying to be written(stored) to
                """
                if i == 'LD':
                    if item[0] == "Loop:":
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
        
                if i == 'DADD':
                    if item[0] == "Loop:":
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
                    
                if i == 'DADDI':
                    if item[0] == "Loop:":
                        dest = item[2]
                        source1 = regs[item[3]]
                        source2 = item[4]
                    else:
                        dest = item[1]
                        source1 = regs[item[2]]
                        source2 = item[3]
#                    dest = item[1]
#                    source1 = regs[item[2]]
#                    source2 = item[3]
                    source2 = source2.translate(None, '#')
                    answer = source1 + int(source2)
                    #print answer
                    regs[dest] = answer
                    
                if i == 'SD':
                    if item[0] == "Loop:":
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
                    
                if i == "BNEZ":
                    loopCount += 1
                    cmp = regs[item[1]]
                    #print cmp
                    if cmp <= 0:
                        go = False
                        #loopCount += 1
                        #break
                    else:
                        go = True
                        #loopCount += 1   
    return loopCount

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

loopCount = 0
loopCount = process(op, memory, regs, loopCount)
print 'loopCount',loopCount

afterBNEZ = []
beforeBNEZ = []
check = ['0', '0']
instructions = []
#place while loop here(old-now in function checkDepend)
loopPlace = []
bnezPlace = []
numLoop = 0

for item in op:
    numLoop += 1
    if item[0] == 'Loop:':
        loopPlace.append(numLoop)
        #numLoop += 1
        #print loopPlace
    if item[0] == 'BNEZ':
        bnezPlace.append(numLoop)
        place = op.index(item)
        #print place
        afterBNEZ = op[place+1:]
        beforeBNEZ = op[0:place+1]
"""
The check for 2 nested loops goes here
"""        
        
print 'numLoop', numLoop
print loopPlace
print bnezPlace
print afterBNEZ
print beforeBNEZ
#print op        
checkDepend(loopCount, beforeBNEZ, instructions)
checkDepend(1, afterBNEZ, instructions)

#print instructions
#print len(instructions)
#print temp
#print regs
#print loopCount    
file.close()
"""
go = True
loopCount = 0
while go == True:
    for item in op:
        for i in item:
            if i == 'Loop:':
                continue
           
           # Need to add checking if R0 is trying to be written(stored) to
            
            if i == 'LD':
                dest = item[2]
                source = item[3]
                result = source.translate(None, ')').split('(')
                loc = int(result[0]) + regs[result[1]]
                memValue = memory[str(loc)]
                #memValue = memory[str(0)]
                regs[dest] = memValue    
    
            if i == 'DADD':
                dest = item[1]
                source1 = regs[item[2]]
                source2 = regs[item[3]]
                #print source1, source2
                answer = source1 + source2
                #print answer
                regs[dest] = answer
                
            if i == 'DADDI':
                dest = item[1]
                source1 = regs[item[2]]
                source2 = item[3]
                source2 = source2.translate(None, '#')
                answer = source1 + int(source2)
                #print answer
                regs[dest] = answer
                
            if i == 'SD':
                temp = item[1]
                addr = temp.translate(None, ')').split('(')
                dest = int(addr[0]) + regs[addr[1]]
                source = regs[item[2]]
                memory[dest] = source
                
            if i == "BNEZ":
                loopCount += 1
                cmp = regs[item[1]]
                #print cmp
                if cmp <= 0:
                    go = False
                    #loopCount += 1
                    #break
                else:
                    go = True
                    #loopCount += 1   
"""
"""
for element in op:
    for item in element:
        for piece in item:
            if piece == ',':
                temp = piece.replace(',', '')
"""
"""            else:
                if i == 'LD':
                    dest = item[2]
                    source = item[3]
                    result = source.translate(None, ')').split('(')
                    loc = int(result[0]) + regs[result[1]]
                    memValue = memory[str(loc)]
                    regs[dest] = memValue
                if i == 'DADD':
                    print "dadd"
                    dest = item[1]
                    source1 = regs[item[2]]
                    source2 = regs[item[3]]
                    #print source1, source2
                    answer = source1 + source2
                    #print answer
                    regs[dest] = answer
                if i == 'DADDI':
                    print "daddi"
                    dest = item[1]
                    source1 = regs[item[2]]
                    source2 = item[3]
                    source2 = source2.translate(None, '#')
                    answer = source1 + int(source2)
                    #print answer
                    regs[dest] = answer
                if i == 'SD':
                    print "sd"
                    temp = item[1]
                    addr = temp.translate(None, ')').split('(')
                    dest = int(addr[0]) + regs[addr[1]]
                    source = regs[item[2]]
                    memory[dest] = source
"""