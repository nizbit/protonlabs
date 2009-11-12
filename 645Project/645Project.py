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
    for line in text:
        line = line.strip()
        words = line.split()
        key = words[0]
        value = words[1]
        dict[key] = value

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

print reg
  
storeInDict(reg, regs)
storeInDict(mem, memory)

op = []
for element in code:
    line = element.strip()
    newline = line.translate(None, ',')
    word = newline.split()
    op.append(word)


for item in op:
    for element in item:
        if element == 'Loop:':
            continue
        else:
            if element == 'LD':
                storeReg = item[2]
                readReg = item[3]
                result = readReg.translate(None, ')').split('(')
                #answer = int(result[0]) + regs[result[1]]
                #print answer  
    
file.close()

"""
for element in op:
    for item in element:
        for piece in item:
            if piece == ',':
                temp = piece.replace(',', '')
"""
