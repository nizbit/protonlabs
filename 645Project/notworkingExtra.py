"""
    Finding the indents
"""
indent = []
for item in code:
    temp = len(item) - len(item.lstrip())
    indent.append(temp)
"""
    Finding code blocks based on indents
"""
parse = []
for x in range(len(indent)-1):
    if indent[x] < indent[x+1]:
        parse.append(x)
    if indent[x] > indent[x+1]:
        parse.append(x)
#parse.append(len(indent)-1)
"""
    Making position of code blocks match
"""
numLoops = len(parse)/2
temp = parse[:numLoops]
temp2 = parse[numLoops:]
temp.reverse()
loop = []
for x in range(len(parse)/2):
    loop.append(temp[x])
    loop.append(temp2[x])

x = 0
loop = []
while x < numLoops:
    #if x == 0:
        
    for y in range(temp[x], temp2[x]+1):
        loop.append(op[y])
    x += 1
print temp
print temp2
print x
print numLoops
print loop
print parse 

"""
    tempstack = []
    orderedop = []
    print numSpaceOp
    x = 0
    while x < len(numSpaceOp)-1:
        #print x
        if numSpaceOp[x] < numSpaceOp[x+1]:
            print '1'
            tempstack.append(op[x])
            x+=1
    
        if numSpaceOp[x] < numSpaceOp[x+1] and numSpaceOp[x+1] == numSpaceOp[x+2]:
            print '4'
            orderedop.append(op[x])
            orderedop.append(op[x+1])
            orderedop.append(op[x+2])
            x+=3
        if numSpaceOp[x] > numSpaceOp[x+1] and numSpaceOp[x+1] == numSpaceOp[x+2]:
            print '4'
            orderedop.append(op[x])
            tempstack.append(op[x+1])
            tempstack.append(op[x+2])
            x+=3
        if numSpaceOp[x] == numSpaceOp[x+1]:
            
        
    #print x              
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
        
    #print tempstack
    #print orderedop
"""
