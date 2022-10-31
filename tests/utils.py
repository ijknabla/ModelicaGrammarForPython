from functools import wraps
from typing import Callable, Dict, Optional, Set, TypeVar

import arpeggio

T_1 = TypeVar("T_1")
T_2 = TypeVar("T_2")


def assert_injective(f: Callable[[T_1], T_2]) -> Callable[[T_1], T_2]:
    ys: Dict[T_2, T_1] = {}

    @wraps(f)
    def wrapped(x: T_1) -> T_2:
        y = f(x)
        assert y not in ys or x == ys[y]
        ys[y] = x
        return y

    return wrapped


def flatten(
    parent: arpeggio.ParsingExpression,
    result: Optional[Dict[str, arpeggio.ParsingExpression]] = None,
) -> Dict[str, arpeggio.ParsingExpression]:
    if result is None:
        result = {}

    if parent.rule_name not in result:

        if parent.rule_name:
            result[parent.rule_name] = parent

        if isinstance(parent, arpeggio.Repetition) and parent.sep is not None:
            flatten(parent.sep, result)

        for child in parent.nodes:
            flatten(child, result)

    return result


def find(
    parent: arpeggio.ParsingExpression,
    ruleName: str,
    unify: Callable[[str], str] = str,
) -> arpeggio.ParsingExpression:
    searched: Set[arpeggio.ParsingExpression] = set()
    candidates = {parent}
    while candidates:
        candidate = candidates.pop()
        if unify(candidate.rule_name) == ruleName:
            return candidate
        if (
            isinstance(candidate, arpeggio.Repetition)
            and candidate.sep is not None
        ):
            candidates.add(candidate.sep)
        candidates.update(candidate.nodes)
        candidates -= searched

    raise ValueError()
