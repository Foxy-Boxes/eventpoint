from dataclasses import dataclass
from typing import List, Union, Literal, ForwardRef

@dataclass(frozen=True)
class ParamStructure:
    type_name: Union[Literal['int'],Literal['bool']]
    param_name: str

@dataclass(frozen=True)
class ExprStructure:
    op: Union[Literal['+'],Literal['-'],Literal['/'],Literal['*'],Literal['&&'],Literal['||'],Literal['=='],Literal['<'],Literal['<='],Literal['>='],Literal['>'], None]
    operand1: Union[str, int, ForwardRef("ExprStructure")]
    operand2: Union[str, int, ForwardRef("ExprStructure"),None]
ConditionStructure = ExprStructure
@dataclass(frozen=True)
class InitStructure:
    tick: int
    random_range: int
    
@dataclass(frozen=True)
class AssignmentStructure:
    assign: str
    expr: ExprStructure


@dataclass(frozen=True)
class TriggerStructure:
    trigger_if: ConditionStructure
    start: str
    args: List[Union[str,int,ExprStructure]]

@dataclass(frozen=True)
class UpdateStructure:
    triggers: List[TriggerStructure]
    update: List[AssignmentStructure]

@dataclass(frozen=True)
class StateStructure:
    state: str
    initial: bool

@dataclass(frozen=True)
class CountStructure:
    state: str
    initial: int

@dataclass(frozen=True)
class StatStructure:
    stat: str
    state: str



@dataclass(frozen=True)
class EventStructure:
    name: str
    tick: int
    random_range: int
    params: List[ParamStructure]
    update: UpdateStructure

@dataclass(frozen=True)
class ProgramStructure:
    decls: List[Union[StateStructure, StatStructure, CountStructure]]
    events: List[EventStructure]
    changes: List[str]
