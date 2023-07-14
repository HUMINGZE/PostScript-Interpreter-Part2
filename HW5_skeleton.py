import re
#------------------------- HW4 Start-------------------------------------

#------------------------- 10% -------------------------------------
# The operand stack: define the operand stack and its operations
opstack = []  #assuming top of the stack is the end of the list

# Now define the helper functions to push and pop values on the opstack
# (i.e, add/remove elements to/from the end of the Python list)
# Remember that there is a Postscript operator called "pop" so we choose
# different names for these functions.
# Recall that `pass` in python is a no-op: replace it with your code.

def opPop():
    return opstack.pop()
    # opPop should return the popped value.
    # The pop() function should call opPop to pop the top value from the opstack, but it will ignore the popped value.

def opPush(value):
    opstack.append(value)

#-------------------------- 20% -------------------------------------
# The dictionary stack: define the dictionary stack and its operations
dictstack = []  #assuming top of the stack is the end of the list

# now define functions to push and pop dictionaries on the dictstack, to
# define name, and to lookup a name

def dictPop():
    return dictstack.pop()
    # dictPop pops the top dictionary from the dictionary stack.

def dictPush(d):
    dictstack.append(d)
    #dictPush pushes the dictionary ‘d’ to the dictstack.
    #Note that, your interpreter will call dictPush only when Postscript
    #“begin” operator is called. “begin” should pop the empty dictionary from
    #the opstack and push it onto the dictstack by calling dictPush.

def define(name, value):
    dictstack.append({name: value})
    #add name:value pair to the top dictionary in the dictionary stack.
    #Keep the '/' in the name constant.
    #Your psDef function should pop the name and value from operand stack and
    #call the “define” function.

def lookup(name):
    names = '/' + name
    for item in dictstack:
        if names in item:
            string = item[names]
    return string
    # return the value associated with name
    # What is your design decision about what to do when there is no definition for “name”? If “name” is not defined, your program should not break, but should give an appropriate error message.


#--------------------------- 10% -------------------------------------
# Arithmetic and comparison operators: add, sub, mul, div, mod, eq, lt, gt
# Make sure to check the operand stack has the correct number of parameters
# and types of the parameters are correct.
def add():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        if isinstance(op1, (int, float)) and isinstance(op2, (int, float)):
            opPush(op1 + op2)
        else:
            print("Error: add - operands must be numbers")
            opPush(op2)
            opPush(op1)
    else:
        print("Error: add expects 2 operands")

def sub():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        if isinstance(op1,int) and isinstance(op2,int):
            opPush(op2 - op1)
        else:
            print("Error: sub - one of the operands is not a number value")
            opPush(op2)
            opPush(op1)             
    else:
        print("Error: add expects 2 operands")

def mul():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        if isinstance(op1,int) and isinstance(op2,int):
            opPush(op2 * op1)
        else:
            print("Error: mul - one of the operands is not a number value")
            opPush(op2)
            opPush(op1)             
    else:
        print("Error: add expects 2 operands")

def div():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        if isinstance(op1, int) and isinstance(op2, int):
            if op1 == 0:
                print("Error: division by zero")
                opPush(op2)
                opPush(op1)
            else:
                opPush(op2 // op1)
        else:
            print("Error: div - one of the operands is not a number value")
            opPush(op2)
            opPush(op1)
    else:
        print("Error: div expects 2 operands")


def mod():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        if isinstance(op1,int) and isinstance(op2,int):
            opPush(op2 % op1)
        else:
            print("Error: mod - one of the operands is not a number value")
            opPush(op2)
            opPush(op1)             
    else:
        print("Error: add expects 2 operands")

def eq():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        if op2 == op1:
            opPush(True)
        else:
            opPush(False)             
    else:
        print("Error")

def lt():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        if op1 > op2:
            opPush(True)
        else:
            opPush(False)             
    else:
        print("Error")

def gt():
    if opPop() < opPop():
        opPush(True)
    else:
        opPush(False)

#--------------------------- 15% -------------------------------------
# String operators: define the string operators length, get, getinterval, put
def length():
    if len(opstack) == 0:
        print("Error")
    else:
        string = opPop()
        opPush(len(string) - 2)

def get():
    if len(opstack) == 0:
        print("Error: Operand stack is empty")
    else:
        index = opPop()
        string = opPop()
        if isinstance(string, str):
            string = string[1:-1]  # Remove the '(' and ')' characters
            opPush(ord(string[index]))
        else:
            print("Error: Invalid operand")

def getinterval():
    if len(opstack) >= 3:
        index1 = opPop()
        index2 = opPop()
        string = opPop()
        if isinstance(index1, int) and isinstance(index2, int) and isinstance(string, str) and string.startswith("(") and string.endswith(")"):
            if 0 <= index2 < len(string) - 2 and index1 >= 0:
                opPush("(" + string[index2 + 1:index2 + index1 + 1] + ")")
            else:
                print("Error: Invalid index")
        else:
            print("Error: Invalid types")
    else:
        print("Error: Should be at least 3 operands")


def put():
    if len(opstack) < 3:
        print("Error: Insufficient operands")
    else:
        replacement_char = opPop()
        index = opPop()
        string = opPop()
        if replacement_char is not None and index is not None and string is not None:
            if isinstance(replacement_char, int) and isinstance(index, int) and isinstance(string, str):
                if string[0] == '(' and string[-1] == ')':
                    content = string[1:-1]
                    if 0 <= index < len(content):
                        content = content[:index] + chr(replacement_char) + content[index + 1:]
                        opPush('(' + content + ')')
                    else:
                        print("Error: Invalid index value")
                else:
                    print("Error: Invalid string format")
            else:
                print("Error: Invalid operand types")
        else:
            print("Error: Invalid operands")


#--------------------------- 25% -------------------------------------
# Define the stack manipulation and print operators: dup, copy, pop, clear, exch, roll, stack
def dup():
    if (len(opstack) == 0):
        print("Error")
    else:
        string = opPop()
        opPush(string)
        opPush(string)

def copy():
    index = opPop()
    newstr = []
    i = i1 = i2 = 0
    for i in range(index):
        string = opPop()
        newstr.append(string)
        i += 1    
    for i1 in range(index):
        opPush(newstr[i - 1])
        i -= 1  
        i1 += 1
    for i2 in range(index):
        opPush(newstr[i - 1])
        i -= 1
        i2+= 1

def pop ():
    if (len(opstack) == 0):
        print("Error")
    else:
        opPop()

def clear():
    opstack.clear()

def exch():
    if len(opstack) > 1:
        op1 = opPop()
        op2 = opPop()
        opPush(op1)
        opPush(op2)
    else:
        print("Error")

def roll():
    if len(opstack) < 2:
        print("Error: Insufficient operands")
    else:
        j = opPop()  # Number of roll operations
        n = opPop()  # Number of elements to roll
        if j is not None and n is not None:
            if isinstance(j, int) and isinstance(n, int) and j >= 0 and n >= 0:
                if len(opstack) >= n:
                    for _ in range(j):
                        opstack[-n:] = opstack[-1:-(n+1):-1]  # Perform the roll operation
                else:
                    print("Error: Not enough elements to roll")
            else:
                print("Error: Invalid operand types")
        else:
            print("Error: Invalid operand(s)")


def stack():
    for i in reversed(opstack):
        print(i)

#--------------------------- 20% -------------------------------------
# Define the dictionary manipulation operators: psDict, begin, end, psDef
# name the function for the def operator psDef because def is reserved in Python. Similarly, call the function for dict operator as psDict.
# Note: The psDef operator will pop the value and name from the opstack and call your own "define" operator (pass those values as parameters).
# Note that psDef()won't have any parameters.

def psDict():
    op = opPop()
    for i in range(op):
        opPush(dict())
        i = i

def begin():
    op = opPop()
    dictstack.append(op)

def end():
    dictPop()

def psDef():
    if len(opstack) == 0:
        print("Error")        
    else:
        op1 = opPop()
        op2 = opPop()
        define(op2, op1)

#------------------------- HW4 END -------------------------------------

def tokenize(s):
    return re.findall("/?[a-zA-Z()][a-zA-Z0-9_()]*|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

# HW5 Requirements: 1.write the Python methods psIf and psIfelse
# 2. write the Python method psFor
# 3. 
# complete this function
# The it argument is an iterator.
# The sequence of return characters should represent a list of properly nested
# tokens, where the tokens between '{' and '}' is included as a sublist. If the
# parenteses in the input iterator is not properly nested, returns False.
def groupMatching2(it):
    res = []
    for c in it:
        if c == '}':
            return False
        elif c=='{':
            # Note how we use a recursive call to group the tokens inside the
            # inner matching parenthesis.
            # Once the recursive call returns the code array for the inner
            # paranthesis, it will be appended to the list we are constructing
            # as a whole.
            res.append(groupMatching2(it))
        else:
            res.append(c)
    return False

def psIf():
    if len(opstack)>1:
        op1 = opPop()
        op2 = opPop()
        if isinstance(op1, dict):
            if isinstance(op2, bool):
                if op2:
                    interpretSPS(op1)
            else:
                print("Error: it should be a boolean")
        else:
            print("Error: it should be a dict")
    else:
        print("Error: ifelse expects 3 operator")

def psIfelse():
    if len(opstack)>2:
        op1 = opPop()
        op2 = opPop()
        op3 = opPop()
        if isinstance(op1,dict):
            if isinstance(op2,dict):
                if isinstance(op3,bool):
                    if op3:
                        interpretSPS(op2)
                    else:
                        interpretSPS(op1)
                else:
                    print("Error: it should be a boolean")
            else:
                print("Error: it should be a dict")
        else:
            print("Error: it should be a dict")
    else:
        print("Error: ifelse expects 3 operator")

def psFor():
    if len(opstack)>3:
        op1 = opPop()
        op2 = opPop()
        op3 = opPop()
        op4 = opPop()
        if isinstance(op1, dict):
            if isinstance(op2, int):
                if isinstance(op3, int):
                    if isinstance(op4, int):
                        indexStart = op4
                        indexEnd = op2
                        if op3 > 0:
                            for x in range(indexStart,indexEnd + 1,op3):
                                opPush(x)
                                interpretSPS(op1)
                        else:
                            for x in range(indexStart,indexEnd - 1,op3):
                                opPush(x)
                                interpretSPS(op1)
                    else:
                        print("Error: start should be int")
                else:
                    print("Error: gap should be int")
            else:
                print("Error: end should be int")
        else:
            print("Error: it should be dict")
    else:
        print("Error: psFor exceed 2 operators")

# Complete this function
# Function to parse a list of tokens and arrange the tokens between { and } braces
# as code-arrays.
# Properly nested parentheses are arranged into a list of properly nested lists.
def parse(L):
    res = []
    it = iter(L)
    for c in it:
        if c=='}':  #non matching closing paranthesis; return false since there is
                    # a syntax error in the Postscript code.
            return False
        elif c=='{':
            res.append(groupMatching2(it))
        else:
            if c.startswith('(') and c.endswith(')'):  # Check if it's a string
                res.append(c)
            else:
                try:
                    num = int(c)  # Try to convert to an integer
                    res.append(num)
                except ValueError:
                    if c.lower() == 'true':
                        res.append(True)
                    elif c.lower() == 'false':
                        res.append(False)
                    else:
                        res.append(c)
    return res


# Write the necessary code here; again write
# auxiliary functions if you need them. This will probably be the largest
# function of the whole project, but it will have a very regular and obvious
# structure if you've followed the plan of the assignment.
#
def interpretSPS(code):
    for item in code:
        if isinstance(item, int) or isinstance(item, bool):
            opPush(item)
        elif isinstance(item, list):
            opPush(item)
        elif isinstance(item, str):
            if item.startswith('/'):
                opPush(item)
            elif item == "add":
                add()
            elif item == "sub":
                sub()
            # Add more conditionals for other built-in operators
            else:
                val = lookup(item)
                if isinstance(val, list):
                    interpretSPS(val)
                elif val is not None:
                    opPush(val)
                else:
                    print("Error!")
        else:
            print("Error!")



# Copy this to your HW5.py file>
def interpreter(s): # s is a string
    interpretSPS(parse(tokenize(s)))


#clear opstack and dictstack
def clear():
    del opstack[:]
    del dictstack[:]


#testing

input1 = """
        /square {
               dup mul
        } def
        (square)
        4 square
        dup 16 eq
        {(pass)} {(fail)} ifelse
        stack
        """

input2 ="""
    (facto) dup length /n exch def
    /fact {
        0 dict begin
           /n exch def
           n 2 lt
           { 1}
           {n 1 sub fact n mul }
           ifelse
        end
    } def
    n fact stack
    """

input3 = """
        /fact{
        0 dict
                begin
                        /n exch def
                        1
                        n -1 1 {mul} for
                end
        } def
        6
        fact
        stack
    """

input4 = """
        /lt6 { 6 lt } def
        1 2 3 4 5 6 4 -3 roll
        dup dup lt6 {mul mul mul} if
        stack
        clear
    """

input5 = """
        (CptS355_HW5) 4 3 getinterval
        (355) eq
        {(You_are_in_CptS355)} if
         stack
        """

input6 = """
        /pow2 {/n exch def
               (pow2_of_n_is) dup 8 n 48 add put
                1 n -1 1 {pop 2 mul} for
              } def
        (Calculating_pow2_of_9) dup 20 get 48 sub pow2
        stack
        """

print(tokenize(input1))
print(parse(tokenize(input1)))

