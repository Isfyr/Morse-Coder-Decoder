import sys

class Node:
    def __init__(self, value = None, left = None, right = None):
        self.left = left
        self.right = right
        self.value = value
#Tree, takes string, converts string into tree
class Tree:
    def __init__(self):
        self.root = None 
        self.index = 0
    allowed_chars = ['*', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 
                         'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    def real_parse(self,string):
        self.index = 0
        string = string.strip()
        return self.parse(string)

    def parse(self, string):#take a string, parse it
        #case: '(', when it hits one of these, do another round of recursion
        while self.index < len(string) and string[self.index] == ' ':
            self.index += 1
        if self.index >= len(string):
            return None
        
        if self.index < len(string) - 1 and string[self.index] == ' ' and string[self.index + 1] == ' ':
            print("ERROR: Invalid tree file.")
            sys.exit()

        if string[self.index] == '(':
            self.index += 1
            left = self.parse(string) #grab left value

            while self.index < len(string) and string[self.index] == ' ':
                self.index += 1

            if string[self.index] not in self.allowed_chars:
                print("ERROR: Invalid tree file.")
                sys.exit()
            value = string[self.index] #add main value
            self.index += 1

            while self.index < len(string) and string[self.index] == ' ': # (1 2 3)
                self.index += 1

            right = self.parse(string)
            
            if self.index < len(string) and string[self.index] == ')':
                self.index += 1
            else:
                print("ERROR: Invalid tree file.")
                sys.exit()
            new_node = Node(value, left, right)
            self.root = new_node
            return new_node
        
        elif string[self.index] in self.allowed_chars:
            value = string[self.index]
            self.index += 1
            new_node = Node(value)
            self.root = new_node
            return new_node
        else:
            print(f"ERROR: Invalid tree file.")
            sys.exit()

    def multiple_check_helper(self, node): #turns into string
        string = ''
        if node is not None:
            string += f"{self.multiple_check_helper(node.left)}"
            string += f" {node.value} "
            string += f"{self.multiple_check_helper(node.right)}"
        return string

    def multiple_check(self): #also contains root asterisk check
        item_list = self.multiple_check_helper(self.root).split()
        for item in item_list:
            if item != '*' and item_list.count(item) > 1:
                print("ERROR: Invalid tree file.")
                sys.exit()
        if self.root.value != '*':
            print("ERROR: Invalid tree file.")
            sys.exit()

    def contains_helper(self, value, node: Node):
        if value == node.value:
            return True
        if node == None:
            return False
        if value < node.value and node.left is not None:
            return self.contains_helper(value,node.left)
        elif value > node.value and node.right is not None:
            return self.contains_helper(value, node.right)

    def __contains__(self, value):
        if self.root is not None:
            return self.contains_helper(value, self.root)

        
    def getmorse(self, node: Node, char, code = ''): #traverse the tree
        if node == None: #if the node is not in the tree
            return ''
        if node.value == char:
            return code
        left_code = self.getmorse(node.left,char, code + '.')
        if left_code:
            return left_code
            
        right_code = self.getmorse(node.right,char, code + '-')
        if right_code:
            return right_code
        
        return ''
   
    def decode(self, node, code, count = 0, space = ''):
        if code == '':
            return space
        if node is None: #if the node is not in the tree
                return '?'
        #search through tree until code is created and then return node.value
          #if value not found, return ?  
        if count == len(code):
            if node.value == '*':
                return '?'
            return space + node.value
        letter = code[count]
        if letter == '.':
            return self.decode(node.left, code, count + 1, space)
        if letter == '-':
            return self.decode(node.right, code, count + 1, space)
        if letter == '/': #then this character is the first in the word
            return self.decode(node.right, code, count + 1, ' ')#want to give space a value
        
        return '?'
        
    def str_helper(self, node: Node):
        string = ''
        
        if node is not None: #base case
            if node.left is None and node.right is None:
                string += f"{node.value}" #no child case
            elif node.left is None:
                string += '(-' #one child case
                string += f" {node.value} "
                string += f"{self.str_helper(node.right)})"
            elif node.right is None: #one child case
                string += f"({self.str_helper(node.left)}"
                string += f" {node.value} "
                string += '-)'
            else: # 2 child case
                string += f"({self.str_helper(node.left)}"
                string += f" {node.value} "
                string += f"{self.str_helper(node.right)})"

        return string
    
    def __str__(self):
        if self.root is None:
            return '-'
        else:
            return self.str_helper(self.root)

number_morse = '(((((5 H 4) S (- V 3)) I (F U (- * 2))) E ((L R -) A (P W (- J 1)))) * ((((6 B -) D X) N (C K Y)) T (((7 Z -) G Q) M ((8 * -) O (9 * 0)))))'
hex = '((((0 * 1) * (2 * 3)) * ((4 * 5) * (6 * 7))) * (((8 * 9) * (A * B)) * ((C * D) * (E * F))))'
morse = '((((H S V) I (F U *)) E ((L R *) A (P W J))) * (((B D X) N (C K Y)) T ((Z G Q) M O)))'
missing_space_morse = '((((H S V) I (FU *)) E ((L R *) A (P W J))) * (((B D X) N (C K Y)) T ((Z G Q) M O)))'
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("USAGE: morse.py [-e or -d] [tree-file]")
    sys.exit()
if len(sys.argv) == 3: # if sys.argv[2] is a proper tree file, use its encoding schema
    if sys.argv[1] =='-e':
        try:
            with open(sys.argv[2], 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("ERROR: Invalid tree file.")
            sys.exit()
        if len(lines) != 1 or len(lines) == 0:
            print("ERROR: Invalid tree file.")
            sys.exit()
        tree_file = lines[0].strip().replace('-', '*')
        cust_encode = Tree()
        cust_encode.real_parse(tree_file)
        cust_encode.multiple_check()
        if tree_file[-1] != ')' or len(tree_file) != len(str(cust_encode)):
            print("ERROR: Invalid tree file.")
            sys.exit()
        for line in sys.stdin: #start looping through lines
            string = ''
            line = line.upper()
            line = line.split()
            for word in line:
                for char in word:
                    m = cust_encode.getmorse(cust_encode.root, char)
                    if m != '':
                        string += m + ' '
                
                string += ' '
            print(string.strip())
            
    elif sys.argv[1] =='-d':
        try:
            with open(sys.argv[2], 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("ERROR: Invalid tree file.")
            sys.exit()
        if len(lines) != 1 or len(lines) == 0:
            print("ERROR: Invalid tree file.")
            sys.exit()
        tree_file = lines[0].strip().replace('-', '*')
        cust_encode = Tree()
        cust_encode.real_parse(tree_file)
        cust_encode.multiple_check()
        if tree_file[-1] != ')' or len(tree_file) != len(str(cust_encode)):
            print("ERROR: Invalid tree file.")
            sys.exit()
        for line in sys.stdin: #start looping through lines
            string = ''
            line = line.strip()
            line = line.replace('  ', '/').split('/') #replace all double spaces with /
            for i in line:
                i = i.strip() 
            for word in line:
                word = word.split()
                for code in word:
                    string += cust_encode.decode(cust_encode.root, code)
                string += ' '
            string = ' '.join(string.split())
            string = string.replace('*', '?')
            print(string)
    else:
        print("USAGE: morse.py [-e or -d] [tree-file]")
        sys.exit()
    
if len(sys.argv) == 2: #use normal encoding schema
    if sys.argv[1] == '-e':
        cust_encode = Tree()
        cust_encode.real_parse(morse)
        for line in sys.stdin: #start looping through lines
            string = ''
            line = line.upper()
            line = line.split()
            for word in line:
                for char in word:
                    m = cust_encode.getmorse(cust_encode.root, char)
                    if m != '':
                        string += m + ' '
                
                string += ' '
            print(string.strip())
    elif sys.argv[1] =='-d':
        cust_encode = Tree()
        cust_encode.real_parse(morse)
        for line in sys.stdin: #start looping through lines
            string = ''
            line = line.strip()
            if '\t' in line:
                line = line.replace('\t', ' ')
            line = line.replace('  ', '/').split('/') #replace all double spaces with /
            for i in line:
                i = i.strip() 
            for word in line:
                word = word.split()
                for code in word:
                    string += cust_encode.decode(cust_encode.root, code)
                string += ' '
            print(' '.join(string.split()))
    else: 
        print("USAGE: morse.py [-e or -d] [tree-file]")
        sys.exit()

