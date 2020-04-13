ac=[]
with open('asm_code.txt') as file:
    for line in file.readlines():
        if (line.find("<") != -1):  # code to remove comments if any #considering a comment if it is followed by    <
            line = line[:line.find("<")]
        line = line.strip()   #removes any leading or follwing spaces and trailing new lines if any(/n)
        ac.append(line)   #creates an list with each line

#print(ac)
#instruction table i.e assembler to opcode one
opt={"STP":"1100", "CLA":'0000', "LAC":'0001',"SAC":'0010',"ADD":'0011', "SUB":'0100',"BRZ":'0101',"BRN":'0110',"BRP":'0111',"INP":'1000',"DSP":'1001',"MUL":'1010',"DIV":'1011'}
#-------------------------initializing stuff----------------------------------------------------------------------------
LC=0  #initializing location counter with 0 #assuming that our code do not have START and we start at 0
errors=""  #this will be a file containg all the errors occuring in the code
er=""    #this contains individual errors
er_c=0    #this variable cantais the number of errors(total error count)
total_length=len(ac)  #this is the total length of the code
lablet=[[],[]]     #lable table(first tuple contains name of lable and second tuple contain address of the lable declared
symbolt=[[],[]]    #inialising symbol table(first tuple contain name of the symbol and se   cond typle contail the address of the variable where it is going to be stored
#-----------------------------getting started with pass one of two pass assembler-------------------------------
#in this whole code i will act like location counter(LC) and vice versa
for i in range(len(ac)):
    words=ac[i].split(" ")
    if(len(words)==1):    # only case would be of CLA and STP
        if(words[0]=="CLA" or words[0]=="STP"):
            LC+=1
            continue
        else:
            er="INVALID OPCODE"+words[0]+"  at line "+str(i)
            errors+=er+"\n"
            er_c+=1
    elif(len(words)==2):
        if (words[0][-1] == ":"):     #conditions if the 1st word is a declaration statement of a literal
            thaw=words[0][:-1]
            if (thaw in opt):
                er="Name of the label"+thaw+" is same as an OPCODE  error at line "+str(i)
                er_c += 1
                errors+=er+"\n"
                continue
            if (thaw in lablet[0]):
                if (lablet[1][lablet[0].index(thaw)]== -1):  # -1 means it is still not declared(therefore we need to declare it with the position)
                    lablet[1][lablet[0].index(thaw)]= LC
                else:                                           #it was going to be declared for another time which should give an error
                    er = "Label \"" + words[0] + "\" has been declared more than once  at line "+str(i)
                    errors += er + "\n"
                    er_c+=1
                    # add to the lable table and continue else report error and continue
            elif(words[1] == "CLA" or words[1] == "STP"):
                lablet[0].append(thaw)
                lablet[1].append(-1)
                LC+=1
                continue
            else:
                er = "Invalid OPCODE = " + words[1]+"  at line "+str(i)
                errors += er + "\n"
                er_c+=1
        else:
            if(words[0] not in opt):
                er = "Invalid OPCODE = " + words[1] + "  at line " + str(i)
                errors += er + "\n"
                er_c += 1
            elif(words[0]=="BRZ" or words[0]=="BRN" or words[0]=="BRP"):
                if(words[1] not in lablet[0]):
                    lablet[0].append(words[1])
                    lablet[1].append(-1)
            elif(words[0]!="CLA" and words[0]!="STP"):
                if (words[1] not in symbolt[0]):
                    symbolt[0].append(words[1])
                    symbolt[1].append(-1)
            else:
                er = "Invalid proceding CODE = " + words[1] + "  at line " + str(i)
                errors += er + "\n"
                er_c += 1
    elif(len(words)==3):             #only case of a declarion statement of a literal
        if (words[0][-1] != ":"):
            er = "Invalid CODE = " + words[0] + "  at line " + str(i)
            errors += er + "\n"
            er_c += 1
        else:
            thaw = words[0][:-1]
            if (thaw in opt):
                er = "Name of the label" + thaw + " is same as an OPCODE" + "  error at line " + str(i)
                er_c += 1
                errors += er + "\n"
                continue
            if (thaw in lablet[0]):
                if (lablet[1][lablet[0].index(thaw)] == -1):  # -1 means it is still not declared(therefore we need to declare it with the position)
                    lablet[1][lablet[0].index(thaw)] = LC
                else:  # it was going to be declared for another time which should give an error
                    er = "Label \"" + words[0] + "\" has been declared more than once" + "at line " + str(i)
                    errors += er + "\n"
                    er_c += 1
                    # add to the lable table and continue else report error and continue
            elif (words[1] != "CLA" or words[1] != "STP"):
                lablet[0].append(thaw)
                lablet[1].append(-1)
            if (words[1] not in opt):
                er = "Invalid OPCODE = " + words[1] + "at line " + str(i)
                errors += er + "\n"
                er_c += 1
            elif (words[1] == "BRZ" or words[1] == "BRN" or words[1] == "BRP"):
                if (words[2] not in lablet[0]):
                    lablet[0].append(words[2])
                    lablet[1].append(-1)
            elif (words[1] != "CLA" and words[1] != "STP"):
                if (words[2] not in symbolt[0]):
                    symbolt[0].append(words[2])
                    symbolt[1].append(-1)
            else:
                er = "Invalid proceding CODE = " + words[1] + "  at line " + str(i)
                errors += er + "\n"
                er_c += 1
    else:
        er = "Invalid length of CODE at line " + str(i)
        errors += er + "\n"
        er_c += 1
if(-1 in lablet[1]):
    er = "Label is used but not defined"
    errors += er + "\n"
    er_c += 1

LC=i+1
#giving address to the variables or symbols
#we assume that we dont need to declare our variables
#the variables will be given memory after we are done with first pass
for j in range(len(symbolt[1])):
    if(symbolt[1][j]==-1):
        symbolt[1][j]=LC
        LC+=1
#--------------defining a function which could take an value(lable or symbol)and return the address in binary format
def giveval(s):
    n=0
    if(s in lablet[0]):
        n=lablet[1][lablet[0].index(s)]          #finding the address from the lable table
    elif(s in symbolt[0]):
        n=symbolt[1][symbolt[0].index(s)]            #finding the address from the symbol table
    v=str(bin(n)[2:])            #this converts to a binary value
    v=((8-len(v))*"0")+v         #our final length should be of 8 bit hence adding addition zeros if needed
    return v
#if we find no errors in pass one we will continue with PASS TWO of the two pass assembler
if(er_c>0):
    print("ERRORS FOUND ON YOUR CODE")
    print(errors)
    print("PLEASE RECTIFY RUN AND RERUN TO CONVERT TO MACHINE CODE")
else:
    print("NO ERRORS FOUND")
    print("--------Label Table---------")
    for i in range(len(lablet[0])):
        print(lablet[0][i],lablet[1][i])
    print("--------Symbol Table--------")
    for i in range(len(symbolt[0])):
        print(symbolt[0][i],symbolt[1][i])
    print("going for second pass :-p")
    objcode=""
    ob=""
    for i in range(len(ac)):
        words = ac[i].split(" ")
        if(len(words)==1):
            ob=opt[words[0]]+"00000000"
        elif(len(words)==2):
            if(words[0][:-1] in lablet[0]):
                ob=opt[words[1]]+"00000000"
            else:
                ob = opt[words[0]]+giveval(words[1])
        elif(len(words)==3):
            ob=opt[words[1]]+giveval(words[1])
        objcode += ob + "\n"

    print("\nFINAL OBJECT CODE\n")

    print(objcode)
    ocText = open("object_code.txt", "w+")       #creating a file to write our final machine code
    ocText.write(objcode)                       #writing our final code