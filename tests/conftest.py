import enum
from typing import Any

import pytest
from arpeggio import EndOfFile, Parser

from modelica_language import ParserPEG, ParserPython
from modelica_language.syntax import v3_4_peg
from modelica_language.syntax.v3_4 import Syntax


@pytest.fixture(scope="module")
def ident_parser() -> ParserPEG:
    return ParserPEG(
        f"""
{v3_4_peg()}
file: IDENT $EOF$
        """,
        "file",
    )


@pytest.fixture(scope="module")
def ident_dialect_parser() -> ParserPEG:
    return ParserPEG(
        f"""
{v3_4_peg()}
IDENT |= r'\\$\\w*'
file: IDENT $EOF$
        """,
        "file",
    )


@pytest.fixture(scope="module")
def peg_file_parser() -> ParserPEG:
    return ParserPEG(
        f"""
{v3_4_peg()}
file: stored-definition $EOF$
        """,
        "file",
        "COMMENT",
    )


@pytest.fixture(scope="module")
def py_file_parser() -> ParserPython:
    def file() -> Any:
        return Syntax.stored_definition, EndOfFile()

    return ParserPython(
        file,
        Syntax.CPP_STYLE_COMMENT,
    )


class ParserParmeter(enum.Enum):
    py = enum.auto()
    peg = enum.auto()


@pytest.fixture(scope="module", params=ParserParmeter)
def file_parser(
    request: pytest.FixtureRequest,
    peg_file_parser: ParserPEG,
    py_file_parser: ParserPython,
) -> Parser:
    param = request.param  # type: ignore
    if param is ParserParmeter.peg:
        return peg_file_parser
    elif param is ParserParmeter.py:
        return py_file_parser
    else:
        raise NotImplementedError()
