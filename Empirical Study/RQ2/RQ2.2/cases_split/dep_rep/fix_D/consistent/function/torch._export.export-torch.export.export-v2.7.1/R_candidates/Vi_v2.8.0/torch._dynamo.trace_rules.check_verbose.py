def check_verbose(obj, is_inlined_call=False):
    if isinstance(
        obj,
        (
            UserFunctionVariable,
            UserMethodVariable,
            NestedUserFunctionVariable,
            LocalGeneratorFunctionVariable,
            LocalGeneratorObjectVariable,
        ),
    ):
        try:
            py_obj = obj.get_function()
        except NotImplementedError:
            py_obj = None
        fi = FunctionInfo(py_obj, obj.get_name(), obj.get_filename(), obj.get_code())
    elif isinstance(obj, types.CodeType):
        fi = FunctionInfo(None, obj.co_name, obj.co_filename, obj)
    elif isinstance(obj, (types.FunctionType, types.MethodType)):
        fi = FunctionInfo(
            obj,
            obj.__name__,
            getfile(obj),
            obj.__code__,  # type: ignore[union-attr] # FIXME Add MethodType.__code__ to typeshed
        )
    else:
        fi = FunctionInfo(obj, None, getfile(obj), None)

    # Consulte the central trace rules defined in torch._dynamo.trace_rules.
    reasons: set[str] = set()
    rule = lookup_inner(fi.py_obj, fi.name, fi.filename, is_inlined_call, reasons)
    if issubclass(
        rule,
        (
            UserFunctionVariable,
            LocalGeneratorFunctionVariable,
            PolyfilledFunctionVariable,
        ),
    ):
        return SkipResult(
            False,
            f"inlined according trace_rules.lookup {reasons.pop()}",
        )
    elif issubclass(rule, TorchInGraphFunctionVariable):
        return SkipResult(
            False,
            f"registered in torch_obj_rule {reasons.pop()}",
        )
    else:
        assert rule == SkipFunctionVariable, rule
        return SkipResult(
            True,
            f"skipped according trace_rules.lookup {reasons.pop()}",
        )
