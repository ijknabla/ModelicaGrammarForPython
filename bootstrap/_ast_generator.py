from ast import (
    AnnAssign,
    Attribute,
    Call,
    ClassDef,
    FunctionDef,
    Import,
    ImportFrom,
    Load,
    Module,
    Name,
    Return,
    Store,
    Subscript,
    Tuple,
    alias,
    arg,
    arguments,
    expr,
    expr_context,
    stmt,
)
from typing import Optional, Sequence, Union


def create_ann_assign(
    target: str,
    annotation: expr,
    value: expr,
) -> AnnAssign:
    return AnnAssign(
        target=create_attribute(target, ctx=Store()),
        annotation=annotation,
        value=value,
        simple=1,
    )


def create_attribute(
    name: str, ctx: Optional[expr_context] = None
) -> Union[Name, Attribute]:
    if ctx is None:
        ctx = Load()
    id, *attrs = name.split(".")
    attribute: Union[Name, Attribute] = Name(id=id, ctx=ctx)
    for attr in attrs:
        attribute = Attribute(value=attribute, attr=attr, ctx=ctx)
    return attribute


def create_call(
    func: str,
    args: Sequence[expr],
) -> Call:
    return Call(
        func=create_attribute(func),
        args=args,
        keywords=[],
    )


def create_function_def(
    name: str,
    args: Sequence[str],
    value: expr,
    decorator_list: Sequence[str],
    returns: str,
) -> FunctionDef:
    return FunctionDef(
        name=name,
        args=arguments(
            posonlyargs=[],
            args=[arg(arg=arg_) for arg_ in args],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[Return(value=value)],
        decorator_list=list(map(create_attribute, decorator_list)),
        returns=create_attribute(returns),
        lineno=None,
    )


def create_module_with_class(
    imports: Sequence[str],
    import_froms: Sequence["tuple[str, Sequence[str]]"],
    class_name: str,
    class_bases: Sequence[str],
    class_body: Sequence[stmt],
) -> Module:
    body: "list[stmt]" = []

    if imports:
        body.append(Import(names=[alias(name=name) for name in imports]))
    if import_froms:
        body.extend(
            [
                ImportFrom(
                    module=module,
                    names=[alias(name=name) for name in names],
                    level=0,
                )
                for module, names in import_froms
            ]
        )

    body.append(
        ClassDef(
            name=class_name,
            bases=[create_attribute(class_base) for class_base in class_bases],
            keywords=[],
            body=class_body,
            decorator_list=[],
        ),
    )

    return Module(
        body=body,
        type_ignores=[],
    )


def create_subscript(
    value: expr,
    slice: expr,
    ctx: Optional[expr_context] = None,
) -> Subscript:
    if ctx is None:
        ctx = Load()
    return Subscript(value=value, slice=slice, ctx=ctx)


def create_tuple(
    elts: Sequence[expr], ctx: Optional[expr_context] = None
) -> Tuple:
    if ctx is None:
        ctx = Load()
    return Tuple(elts=elts, ctx=ctx)
