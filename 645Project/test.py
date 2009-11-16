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

numSpaceOp = []
for item in code:
    temp = len(item) - len(item.lstrip())
    numSpaceOp.append(temp)

tempstack = []
orderedop = []

x = 0
while x < len(numSpaceOp)-1:
    if numSpaceOp[x] < numSpaceOp[x+1]:
        tempstack.append(op[x])

    if  numSpaceOp[x] < numSpaceOp[x+1] and numSpaceOp[x+2] == numSpaceOp[x+3]:
        orderedop.append(op[x+1])
        orderedop.append(op[x+2])
        orderedop.append(op[x+3])
        x+=4
        break
    x+=1
                    
#for x in range(len(numSpaceOp)-1):
#    print x
#    if numSpaceOp[x] < numSpaceOp[x+1]:
#        tempstack.append(op[x])
#        orderedop.append(op[x+1])
#    elif numSpaceOp[x] > numSpaceOp[x+1]:
#        pass
#    elif numSpaceOp[x] == numSpaceOp[x+1]:
#        orderedop.append(op[x+1])
    #if numSpaceOp[x+1] == numSpaceOp[x]:
     #   orderedop.append(op[x+1])
    
print tempstack
print orderedop

file.close()
