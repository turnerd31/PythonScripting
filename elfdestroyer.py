"""
.Synopsis
    If an elf binary has a main function, this script will disassemble it and display opcodes at memory locations. As a bonus this script will also display binary section names and locations

    Author: Drew Turner
    Required Dependencies: Elftools and Capstone
    Updated: June 2019

.DESCRIPTION
    This script provides a simplified way to display binary functions with Python

.EXAMPLE
    python elfdestroyer.py example.elf

.NOTES
   Not perfect, but was a fun learning experience

"""

from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection
from capstone import *
import sys
binaryname = sys.argv[1]
findmain = None
symbols={}


#def relocations():
print("-----relocation names and locations---------")
with open(binaryname, 'rb') as f:
        e = ELFFile(f)
        for section in e.iter_sections():
            if isinstance(section, RelocationSection):
                print('{0}:'.format(section.name))
                symbol_table = e.get_section(section['sh_link'])
                for relocation in section.iter_relocations():
                    symbol = symbol_table.get_symbol(relocation['r_info_sym'])
                    addr = hex(relocation['r_offset'])
                    print('{0} {1}'.format(symbol.name,addr))
                    symbols [symbol.name] = addr
                    #if "main" in symbol.name:
                            #print("This looks like the main function!!!!")
                            #print(type(symbol.name))
                            #print(addr)
                            #findmain = addr
#    return
#findmain = relocations()
print("---------reprinting.....looking for the main function-------------")
for key in symbols.keys():
        print(key)
        if "main" in key:
            print("This looks like the main function!!!!")
            findmain = symbols[key]
            findmain = int(findmain, 16)

def sections():
    with open(binaryname, 'rb') as f:
        e = ELFFile(f)
        for section in e.iter_sections():
            print(hex(section['sh_addr']), section.name)
    return

def disas():
    with open(binaryname, 'rb') as f:
        elf = ELFFile(f)
        code = elf.get_section_by_name('.text')
        ops = code.data() # returns a bytestring with the opcodes
        addr = code['sh_addr'] # starting address of `.text`
        md = Cs(CS_ARCH_X86, CS_MODE_64)

        for i in md.disasm(ops, findmain):  # looping through each opcode
            for key, value in symbols.items():
                if int(value,16) == i.address:
                    relocationkey = key
                    print("0x{0}:\t{1}\t{2}\t{3}".format(i.address,i.mnemonic,i.op_str,relocationkey))

                if value == i.op_str:
                    opkey = key
                    print("0x{0}:\t{1}\t{2}\t{3}".format(i.address,i.mnemonic,i.op_str,opkey))

            print("0x{0}:\t{1}\t{2}".format(i.address,i.mnemonic,i.op_str,))

    return
print("--Sections of the binary--")
sections()
print("--Disasemble of binary at Main Function location--")
disas()
