from sly import Lexer
class EventLexer(Lexer):
    tokens = { TRIGGER, IF, EVENT, NUMBER, STATE, COUNT, ID, TICK, RANGE, STAT, INT, BOOL, PARAM, GE,LE,EQ,NE,AND,OR, CHANGE }
    ignore = ' \t\n'
    literals = { '=', '+', '-', '*', '/', '(', ')', ';', ',', '{', '}', '<', '>' }

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    GE = r'>='
    LE = r'<='
    EQ = r'=='
    NE = r'!='
    AND = r'\&\&'
    OR = r'\|\|'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['trigger'] = TRIGGER
    ID['if'] = IF
    ID['event'] = EVENT
    ID['state'] = STATE
    ID['count'] = COUNT
    ID['tick'] = TICK
    ID['range'] = RANGE
    ID['stat'] = STAT
    ID['int'] = INT
    ID['bool'] = BOOL
    ID['param'] = PARAM
    ID['change'] = CHANGE
