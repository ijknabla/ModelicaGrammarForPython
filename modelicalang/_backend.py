__all__ = (
    "ClassVar",
    "Optional",
    "ParsingExpressionLike",
    "RegExMatch",
    "SyntaxMeta",
    "Tuple",
    "ZeroOrMore",
    "not_start_with_keyword",
    "returns_parsing_expression",
)

import builtins
import types
from functools import wraps
from types import TracebackType
from typing import TYPE_CHECKING, Any, Callable, ClassVar
from typing import Optional as NoneOr
from typing import Tuple, Type, TypeVar, cast

from arpeggio import Not, Optional, ParsingExpression, RegExMatch, ZeroOrMore
from typing_extensions import ParamSpec, Protocol

if TYPE_CHECKING:
    from . import ParsingExpressionLike
else:
    ParsingExpressionLike = "ParsingExpressionLike"

P = ParamSpec("P")
T = TypeVar("T")
T_keywords = TypeVar("T_keywords", bound="SupportsKeywords")


class SupportsKeywords(Protocol):
    _keywords_: ClassVar[Tuple[str, ...]]


def returns_parsing_expression(
    f: Callable[P, ParsingExpressionLike]
) -> Callable[P, ParsingExpression]:
    return cast(Callable[P, ParsingExpression], f)


def not_start_with_keyword(
    f: Callable[[Type[T_keywords]], ParsingExpression]
) -> Callable[[Type[T_keywords]], ParsingExpression]:
    @wraps(f)
    @returns_parsing_expression
    def wrapped(cls: Type[T_keywords]) -> ParsingExpressionLike:
        return (
            Not(
                RegExMatch(
                    r"(" + r"|".join(cls._keywords_) + r")(?![0-9A-Z_a-z])"
                )
            ),
            f(cls),
        )

    return wrapped


_isinstance__builtins = builtins.isinstance


def _isinstance__callable_as_function(obj: Any, class_or_tuple: Any) -> bool:
    if class_or_tuple is types.FunctionType:  # noqa: E721
        return _isinstance__builtins(obj, Callable)  # type: ignore
    else:
        return _isinstance__builtins(obj, class_or_tuple)


def _isinstance__callable_as_function_is_enabled() -> bool:
    return builtins.isinstance is _isinstance__callable_as_function


class SyntaxMeta(type):
    def __enter__(cls) -> "SyntaxMeta":
        if not _isinstance__callable_as_function_is_enabled():
            builtins.isinstance = _isinstance__callable_as_function
        return cls

    def __exit__(
        cls,
        typ: NoneOr[Type[BaseException]],
        value: NoneOr[BaseException],
        traceback: NoneOr[TracebackType],
    ) -> NoneOr[bool]:
        builtins.isinstance = _isinstance__builtins
        return None
