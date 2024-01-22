from sly import Parser
from lex import EventLexer
from structures import *



class EventParser(Parser):
    tokens = EventLexer.tokens

    @_('decl_list event_list change_list')
    def program(self, p):
        return ProgramStructure(p.decl_list, p.event_list, p.change_list)
    @_('EVENT ID "{" init ";" update "}"')
    def event(self, p):
        ev = EventStructure(p.ID, p.init.tick, p.init.random_range,[], p.update)
        return ev
    
    @_('EVENT ID PARAM param_list "{" init ";" update "}"')
    def event(self, p):
        ev = EventStructure(p.ID, p.init.tick, p.init.random_range,p.param_list, p.update)
        return ev
    @_('TRIGGER IF expr ID "(" args_list ")"')
    def trigger(self, p):
        return TriggerStructure(p.expr, p.ID, p.args_list)
    @_('empty')
    def trigger_list(self, p):
        return []
    @_('trigger')
    def trigger_list(self, p):
        return [p.trigger]
    @_('trigger "," trigger_list')
    def trigger_list(self, p):
        return [p.trigger] + p.trigger_list
    @_('empty')
    def args_list(self, p):
        return []
    @_('arg')
    def args_list(self, p):
        return [p.arg]
    @_('args_list "," arg')
    def args_list(self, p):
        return p.args_list + [p.arg]
    @_('NUMBER','ID','expr')
    def arg(self, p):
        return p[0]

    @_('INT ID')
    def param(self, p):
        return ParamStructure('int', p.ID)

    @_('BOOL ID')
    def param(self, p):
        return ParamStructure('bool', p.ID)

    @_('param_list "," param')
    def param_list(self, p):
        return p.param_list + [p.param]
    
    @_('param')
    def param_list(self, p):
        return [p.param]
    
    @_('TICK NUMBER RANGE NUMBER')
    def init(self,p):
        return InitStructure(p.NUMBER0, p.NUMBER1)
    
    @_('trigger_list ";" assignment_list')
    def update(self, p):
        return UpdateStructure(p.trigger_list, p.assignment_list)
    
    @_('')
    def empty(self, p):
        return []
    @_('empty')
    def assignment_list(self, p):
        return []

    @_('assignment_list assignment')
    def assignment_list(self, p):
        return p.assignment_list + [p.assignment]

    @_('ID "=" expr ";"')
    def assignment(self, p):
        return AssignmentStructure(p.ID, p.expr)
    
    @_('mexpr')
    def aexpr(self, p):
        return p.mexpr
    @_('aexpr "+" mexpr',
       'aexpr "-" mexpr')
    def aexpr(self, p):
        return ExprStructure(p[1],p.aexpr, p.mexpr)

    @_('prim')
    def mexpr(self, p):
        return p.prim
    @_('mexpr "*" prim',
       'mexpr "/" prim')
    def aexpr(self, p):
        return ExprStructure(p[1],p.mexpr, p.prim)

    @_('aexpr')
    def rexpr(self, p):
        return p.aexpr
    @_('rexpr "<" aexpr',
       'rexpr ">" aexpr',
       'rexpr GE aexpr',
       'rexpr LE aexpr')
    def rexpr(self, p):
        return ExprStructure(p[1],p.rexpr, p.aexpr)

    @_('rexpr')
    def eexpr(self, p):
        return p.rexpr
    @_('eexpr EQ rexpr',
       'eexpr NE rexpr')
    def eexpr(self, p):
        return ExprStructure(p[1],p.eexpr, p.rexpr)
    
    @_('eexpr')
    def landexpr(self, p):
        return p.eexpr
    @_('landexpr AND eexpr')
    def landexpr(self, p):
        return ExprStructure('&&',p.landexpr, p.eexpr)

    @_('landexpr')
    def lorexpr(self, p):
        return p.landexpr
    @_('lorexpr OR landexpr')
    def lorexpr(self, p):
        return ExprStructure('||',p.lorexpr, p.landexpr)
    
    @_('lorexpr')
    def expr(self, p):
        return p.lorexpr

    @_('NUMBER', 'ID')
    def prim(self, p):
        return ExprStructure(None, p[0], None)
    @_('"(" expr ")"')
    def prim(self, p):
        return p.expr

    @_('STATE ID "=" NUMBER ";"')
    def state(self, p):
        return StateStructure(p.ID, bool(p.NUMBER))

    @_('COUNT ID "=" NUMBER ";"')
    def count(self, p):
        return CountStructure(p.ID, p.NUMBER)
    
    @_('STAT ID "=" ID ";"')
    def stat(self, p):
        return StatStructure(p.ID0, p.ID1)

    @_('stat', 'count', 'state')
    def decl(self, p):
        return p[0]

    @_('empty')
    def decl_list(self, p):
        return []

    @_('decl_list decl')
    def decl_list(self, p):
        return p.decl_list + [p.decl]

    @_('empty')
    def event_list(self, p):
        return []
    
    @_('event_list event')
    def event_list(self, p):
        return p.event_list + [p.event]
    @_('CHANGE ID ";"')
    def change(self, p):
        return p.ID
    @_('change_list change')
    def change_list(self, p):
        return p.change_list + [p.change]
    @_('empty')
    def change_list(self, p):
        return []


