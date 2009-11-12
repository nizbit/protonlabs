import tkFileDialog

def extract(text, sub1, sub2):
    """
    extract a substring from text between first
    occurances of substrings sub1 and sub2
    """
    temp = text.split(sub1, 1)[-1].split(sub2, 1)[0]
    temp = temp.strip()
    return temp.split("\n")

def storeInDict(text, dict):
    for line in text:
        line = line.rstrip()
        words = line.split(' ')
        if len(words) == 1:
            continue
        
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

op = []
for element in code:
    line = element.strip()
    word = line.split('\r')
    op.append(word)
    

print op
    
storeInDict(reg, regs)
storeInDict(mem, memory)
    
file.close()