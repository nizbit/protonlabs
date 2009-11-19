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

def process(op, memory, regs, loopCount):
    go = True
    loop = 0
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
                    loop += 1
                    cmp = regs[item[1]]
                    #print cmp
                    if cmp <= 0:
                        go = False
                        #loopCount += 1
                        #break
                    else:
                        go = True
                        #loopCount += 1   

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

process(op,memory,regs,0)
print regs


file.close()