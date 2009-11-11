import tkFileDialog

file = tkFileDialog.askopenfile(title="Open input data file",
                                mode='r',
                                filetypes=[("all formats", "*")])
regs = {}
for x in range(32):
    key = 'R' + str(x)
    regs[key] = 0

memory = {}
for x in range(0, 992, 8):
    memory[x] = 0

for line in file:
    line = line.rstrip()
    words = line.split(' ')
    #print words
    

file.close()
#print line