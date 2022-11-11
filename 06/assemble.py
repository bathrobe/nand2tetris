# step by step:
with open('./pong/Pong.asm') as f:
    lines = f.readlines()
pure_code = []
for line in lines:
    if(line[0] != "\n") and (line[0] != "/" and line[1] != "/"):
        line = line.replace(" ", "")
        charlist = [*line]
        if "//" in line:
            first_slash = 0
            for idx, char in enumerate(charlist):
                if(char == "/" and first_slash == 0):
                    first_slash = idx
            charlist = charlist[:first_slash]  
        if("\n" in charlist):
            charlist.remove("\n")
        pure_code.append(charlist)

# symbol table
# kinds of symbols: @name to designate a memory location
# (POINT) in the code to grab the line number
# @R1 , @KBD etc for predefined vars
symbol_table = {"R0": "0", "R1": "1","R2": "2","R3": "3", "R4": "4","R5": "5","R6": "6","R7": "7","R8": "8","R9": "9","R10": "10","R11": "11","R12": "12","R13": "13","R14": "14","R15": "15", "KBD":"24576","SCREEN":"16384","SP":"0","LCL":"1","ARG":"2","THIS":"3","THAT":"4"}
def label_parser(pure_code):
    # first pass grabs the labels
    label_parsed_code = pure_code
    for idx, line in enumerate(label_parsed_code):
        if(type(line) == int):
            line = [line]
        if("(" in line and ")" in line):
            line.remove("(")
            line.remove(")")
            stringed_index = '@' + str(idx)
            symbol_table[''.join(line)] = [*stringed_index]
            if(label_parsed_code is not None):
                label_parsed_code.remove(line)
    # second pass adds symbols to symbol table
    n = 14
    for idx, line in enumerate(label_parsed_code):
        if line[0] == '@':
            # if there are any letters in the stuff after @
            sym = "".join(line[1:])
            if(any(char.isalpha() for char in line[1:])):
                if(sym in symbol_table):
                    if type(symbol_table[sym]) == str:
                        stridx = '@' + symbol_table[sym]
                        symbol_table[sym] = [*stridx]
                else:
                    symbol_table[sym] = [*str('@' + str(n))]
                    n = n+1
                pure_code[idx] = symbol_table[sym]# take the sym string and turn it into a list of characters
    return label_parsed_code
# parser unpacks each instruction into its underlying fields
# list of dictionaries that holds all the parsed assembly instructions
assemblyInstructions = []
# two functions here A commands and C commands, respectively
# the functions take in a single line from the code parsed line by line
def a_command(line):
    address = []
    for char in line:
     if(char != "@" and char != "\n"):
        if(isinstance(address, str)):
            address = [address]
        address.append(char)
        address = "".join(address)
        a_dict = {"type": "A", "parsed_assembly_instruction": address}
    return a_dict

def c_command(line):
    command = {"type": "C", "parsed_assembly_instruction": {"C": [], "D": [], "J": []}}
    # doing the D instruction
    # all up to the equal sign
    D_instruction = [] 
    equals_sign_index = 0 
    for idx, x in enumerate(line):
    # if line does not contain =, grab up until the semicolon_idx
    # move semicolon_idx up to here
        if(x == "="):
            equals_sign_index = idx

    semicolon_idx = -1
    for idx, x in enumerate(line):
        if(x == ';'):
            semicolon_idx = idx

    for idx, x in enumerate(line):
        # print(f"idx {idx} x {x} line {line} equals_sign_index {equals_sign_index}")
        if(idx < equals_sign_index):
            if(x != "=" ):
                # print("this x has been selected", x)
                D_instruction.append(x)
    command["parsed_assembly_instruction"]["D"] = D_instruction
    semicolon_idx = -1
    C_instruction = []
    for idx, x in enumerate(line):
        if(x == ';'):
            semicolon_idx = idx

    for idx, x in enumerate(line):
        if((x != "=" and idx > equals_sign_index and x != "\n") or '=' not in line):
            if((semicolon_idx == -1 or idx < semicolon_idx) ):
# and idx < semicolon_idx
#  or "=" not in line
                C_instruction.append(x)
    if(C_instruction == []):
        C_instruction = ["null"]
    command["parsed_assembly_instruction"]["C"] = C_instruction

    J_instruction = []
    for idx, x in enumerate(line):
        if(idx > semicolon_idx and semicolon_idx != -1):
            J_instruction.append(x)
    command["parsed_assembly_instruction"]["J"] = J_instruction

    return command

# dictionary to look up C commands
c_dict = {
        "D": {"null": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110", "AMD": "111" }, "C": {"0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001", "-D":"0001111", "-A":"0110011", "D+1":"0011111", "A+1":"0110111", "D-1":"0001110", "A-1": "0110010", "D+A":"0000010", "D-A":"0010011", "A-D":"0000111", "D&A":"0000000", "D|A":"0010101","M":"1110000", "!M":"1110001", "-M":"1110011", "M+1":"1110111", "M-1":"1110010", "D+M":"1000010", "D-M":"1010011", "M-D":"1000111", "D&M":"1000000", "D|M": "1010101"
            }, "J": {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP":"111"}
        }


def parser(raw_code):
    for idx, line in enumerate(raw_code):
        if(line[0] == "@"):
            if type(line) == int:
                line = [str(line)]
            # if it contains letters, run it through the symbol table
            parsed_address = a_command(line);
            assemblyInstructions.append(parsed_address)
        elif(line[0] != "@" and "(" not in line and ")" not in line):
            parsed_command = c_command(line)
            #parsed_command = ""
            assemblyInstructions.append( parsed_command)
    return assemblyInstructions

# code that translates each field into its corresponding binary value
def encoder(assemblyInstructions):
    binaryInstructions = []
    for idx, line in enumerate(assemblyInstructions):
        code = line["parsed_assembly_instruction"]
        if(line["type"] == "A"):
            if(not any(char.isalpha() for char in code)):
                address_in_binary = bin(int(code)).replace("0b", "")
                byte = ("0" * (16 - len(address_in_binary))) + address_in_binary
                binaryInstructions.append(byte)
        if(line["type"] == "C"):
            bin_c = "111"
            if(code['C'] == []):
                assembly_c = "null"
            else:
                assembly_c = "".join(code["C"])
            try:
                bin_c += c_dict["C"][assembly_c]
            except KeyError:
                print("key error, your command", assembly_c, " was not found (from line ", line, "index:", idx)
            if(code['D'] == []):
                assembly_d = "null"
            else:
                assembly_d = "".join(code['D'])
            bin_c += c_dict['D'][assembly_d]
            if(code['J'] == []):
                assembly_j = "null"
            else:
                assembly_j = "".join(code["J"])
            bin_c += c_dict["J"][assembly_j]
            binaryInstructions.append(bin_c)
    return binaryInstructions
# symbol table
# main initializes i/0 
def main():
    label_parsed_code = label_parser(pure_code)
    assembly = parser(label_parsed_code)
    binary = encoder(assembly)
    f = open("pongWithSymbols.hack", "w")
    f.write("\n".join(binary))
    f.close()
main()
