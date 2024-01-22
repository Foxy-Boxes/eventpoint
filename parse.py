from parser import EventParser
from lex import EventLexer
from process import process
import sys

if __name__ == '__main__':
    lexer = EventLexer()
    parser = EventParser()
    if len(sys.argv) != 3:
        exit(-1)
    with open(sys.argv[2], 'r') as f:
        x = f.read()
        with open('register.h','w') as w:
            w.write(process(parser.parse(lexer.tokenize(x))))
