from structures import *
from string import Template

states = []
state_resets = []
params = []
int_param_names = []
bool_param_names = []
state_names = []
event_names = []

event_inits = ""
dispatch_codes = ""
dispatch_registers = ""
start_funcs = ""

def process(program: ProgramStructure):
    global states
    global params
    global int_param_names
    global bool_param_names
    global state_names
    global event_names
    global event_inits
    global dispatch_codes
    global dispatch_registers
    global start_funcs

    for decl in program.decls:
        if(type(decl) == StateStructure):
            initial = str(decl.initial).lower()
            states.append('bool {state} = {initial};'.format(state=decl.state, initial = initial))
            state_names.append(decl.state)
            state_resets.append('{state} = {initial};'.format(state=decl.state, initial = initial))
        if(type(decl) == CountStructure):
            states.append('int {state} = {initial};'.format(state=decl.state, initial = decl.initial))
            state_names.append(decl.state)
            state_resets.append('{state} = {initial};'.format(state=decl.state, initial = decl.initial))
    for i,event in enumerate(program.events):
        int_param_names_event = []
        bool_param_names_event = []
        for param in event.params:
            if param.type_name == 'int':
                int_param_names_event.append(param.param_name)
            if param.type_name == 'bool':
                bool_param_names_event.append(param.param_name)
        int_param_names.append(int_param_names_event)
        bool_param_names.append(bool_param_names_event)
        event_names.append(event.name)
        params.append(event.params)
        with open("event_init.ftemplate", 'r') as f:
            src = Template(f.read())
            res = src.substitute({
                'event_index': i,
                'tick': (event.tick),
                'range': (event.random_range)
                })
            event_inits = event_inits + res + "\n"
    dispatch_file = open("dispatch.ftemplate", "r")
    dispatch_template = Template(dispatch_file.read())
    trigger_file = open("trigger.ftemplate", "r")
    trigger_template = Template(trigger_file.read())
    dispatchr_file = open("dispatch_register.ftemplate", "r")
    dispatchr_template = Template(dispatchr_file.read())
    start_file = open("start.ftemplate", "r")
    start_template = Template(start_file.read())
    for i,event in enumerate(program.events):
        int_param_names_event = int_param_names[i]
        bool_param_names_event = bool_param_names[i]
        triggers = ""
        for trigger in event.update.triggers:
            condition = expr_translate(trigger.trigger_if, int_param_names_event, bool_param_names_event)
            try:
                next_event = event_names.index(trigger.start)
            except:
                raise NameError('Event {e} not found'.format(e=trigger.start))
            param_init = find_params(next_event, trigger.args, int_param_names_event, bool_param_names_event)
            trigger_code = trigger_template.substitute({
                "condition": condition,
                "next_event": next_event,
                "name": event_names[next_event],
                "param_init": param_init,
                })
            triggers = triggers + trigger_code +"\n"
        update = ""
        f_str = "{lval} = {rval};\n"
        for assignment in event.update.update:
            rval = expr_translate(assignment.expr, int_param_names_event, bool_param_names_event)
            update = update + f_str.format(lval = assignment.assign, rval = rval)
        dispatch_code = dispatch_template.substitute({
                "event_index": i,
                "triggers": triggers,
                "update": update
            })
        dispatch_codes = dispatch_codes + dispatch_code + "\n"
        dispatch_register = dispatchr_template.substitute({
                "event_index":i
            })
        dispatch_registers = dispatch_registers + dispatch_register + "\n"
        param_list = []
        parameter = "{type_name} {name}"
        param_init_start = "params->int_params.resize({});\nparams->bool_params.resize({});\n".format(len(int_param_names_event),len(bool_param_names_event))
        parameter_init = "params->{type_name}_params[{ind}] = {name};\n"
        for param in event.params:
            param_list.append(parameter.format(type_name=param.type_name, name = param.param_name))
            if param.type_name == 'bool':
                ind = bool_param_names_event.index(param.param_name)
                parameter_i = parameter_init.format(type_name="bool",ind=ind, name = param.param_name)
            else:
                ind = int_param_names_event.index(param.param_name)
                parameter_i = parameter_init.format(type_name="int",ind=ind, name = param.param_name)
            param_init_start = param_init_start + parameter_i
        start_func = start_template.substitute({
                "event_name": event.name,
                "param_list": ",".join(param_list),
                "event_index": i,
                "param_init": param_init_start
            })
        start_funcs = start_funcs + start_func + "\n"
    tick_changes = ""
    change_file = open('change.ftemplate', 'r')
    change_template = Template(change_file.read())
    for name in program.changes:
        try:
            index = event_names.index(name)
            tick_change = change_template.substitute({
                    "event_name":name,
                    "event_index":index
                })
            tick_changes = tick_changes + tick_change + "\n"
        except:
            raise NameError("No event named {name}".format(name=name))
    with open('register.htemplate', 'r') as f:
        r_t = Template(f.read())
        res = r_t.substitute({
            "num_events": len(program.events),
            "state_variables": "\n".join(states),
            "event_dispatch_codes": dispatch_codes,
            "event_dispatch_register": dispatch_registers,
            "event_init": event_inits,
            "state_reset": "\n".join(state_resets),
            "start_funcs": start_funcs,
            "tick_changes": tick_changes
            })
        return res
def find_args(expr: ExprStructure):
    if expr.op == None:
        return str(expr.operand1)
    op1 = find_args(expr.operand1)
    op2 = find_args(expr.operand2)
    return "(" + op1 + ") " + expr.op + " (" + op2 + ")"


def find_params(index: int,args:List[AssignmentStructure], int_param_names_event: List[str], bool_param_names_event: List[str]):
    global params
    global int_param_names
    global bool_param_names
    init = "params->int_params.resize({s1});\nparams->bool_params.resize({s2});\n".format(s1=len(int_param_names[index]), s2=len(bool_param_names[index]))
    for i,arg in enumerate(args):
        if (type(arg) == ExprStructure):
            val = expr_translate(arg,int_param_names_event,bool_param_names_event)
        elif type(arg) == str:
            val = expr_translate(ExprStructure(None,arg,None),int_param_names_event,bool_param_names_event)

        else:
            val = arg

        f_str = 'params->{type_name}_params[{ind}] = {val};\n'
        try:
            lindex = int_param_names[index].index(params[index][i].param_name)
            init = init + f_str.format(type_name='int', ind=lindex,val=val) 
            continue
        except:
            if index == 0:
                print("not int", i)
            pass
        try:
            lindex = bool_param_names[index].index(params[index][i].param_name)
            init = init + f_str.format(type_name='bool', ind=lindex,val=val)
        except:
            if index == 0:
                print("not bool", i)
            pass
    return init 

    


def expr_translate(expr: ExprStructure, int_param_names_event: List[str], bool_param_names_event: List[str]):
    global state_names
    if expr.op == None:
        if type(expr.operand1) == str:
            if expr.operand1 in state_names:
                return expr.operand1
            f_str = 'tick_ev.params->{type_name}_params[{ind}]'
            try:
                index = int_param_names_event.index(expr.operand1)
                return f_str.format(type_name="int", ind = index)
            except:
                pass
            try:
                index = bool_param_names_event.index(expr.operand1)
                return f_str.format(type_name="bool", ind = index)
            except:
                raise NameError('parameter does not exist') 
        return str(expr.operand1)
    op1 = expr_translate(expr.operand1, int_param_names_event, bool_param_names_event)
    op2 = expr_translate(expr.operand2, int_param_names_event, bool_param_names_event)
    return "(" + op1 + ") " + expr.op + " (" + op2 + ")"

    

