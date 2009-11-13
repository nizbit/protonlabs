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

file = tkFileDialog.askopenfile(title="Open input data file",
                                mode='r',
                                filetypes=[("all formats", "*")])
regs = {}
for x in range(32):
    key = 'R' + str(x)
    regs[key] = 0

memory = {}
for x in range(0, 992, 8):
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

go = True
loopCount = 0
while go == True:
    for item in op:
        for i in item:
            if i == 'Loop:':
                continue
            else:
                if i == 'LD':
                    dest = item[2]
                    source = item[3]
                    result = source.translate(None, ')').split('(')
                    loc = int(result[0]) + regs[result[1]]
                    memValue = memory[str(loc)]
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
                cmp = regs[item[1]]
                if cmp == 0:
                    go = False
                    loopCount += 1
                    #break
                else:
                    go = True
                    loopCount += 1   

print regs
print loopCount    
file.close()

"""
for element in op:
    for item in element:
        for piece in item:
            if piece == ',':
                temp = piece.replace(',', '')
"""
