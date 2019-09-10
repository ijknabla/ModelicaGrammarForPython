
__all__ = (
    "PrimitiveReal",
    "PrimitiveInteger",
    "PrimitiveString",
)

import numpy
from .. import util
from .abc import AbstractModelicaScalarClass

RealType = numpy.double
IntegerType = numpy.intc
StringType = str


class ScalarNumberMeta(
    AbstractModelicaScalarClass,
):
    def __new__(mtcls, name, bases, namespace):
        base_class_forward = util.Forward()
        def newfunc(cls, *args, **kwrds):
            with base_class_forward as base_class:
                self = super(base_class, cls).__new__(
                    cls, *args, **kwrds
                )
            
            if not isinstance(self, cls):
                raise ValueError(
                    f"{self}: {type(self)} is not instance of {cls}"
                )

            return self

        namespace["__new__"] = newfunc

        cls = base_class_forward << (
            super(ScalarNumberMeta, mtcls).__new__(
                mtcls,
                name,
                bases,
                namespace,
            )
        )

        return cls


class PrimitiveReal(
    RealType,
    metaclass=ScalarNumberMeta
):
    pass


class PrimitiveInteger(
    IntegerType,
    metaclass=ScalarNumberMeta,
):
    pass


class PrimitiveString(
    str,
    metaclass=AbstractModelicaScalarClass,
):
    def __format__(self, format_spec):
        replaced = util.replace_all(
            self,
            [
                ("\\", r"\\"),
                ('\"', r'\"'),
                ("\a", r"\a"),
                ("\b", r"\b"),
                ("\f", r"\f"),
                ("\n", r"\n"),
                ("\t", r"\t"),
                ("\v", r"\v"),
            ],
        )

        double_quoted = f'"{replaced}"'
    
        return f"{double_quoted:{format_spec}}"
