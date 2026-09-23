def export(
    mod: torch.nn.Module,
    args: tuple[Any, ...],
    kwargs: Optional[dict[str, Any]] = None,
    *,
    dynamic_shapes: Optional[Union[dict[str, Any], tuple[Any], list[Any]]] = None,
    strict: bool = False,
    preserve_module_call_signature: tuple[str, ...] = (),
) -> ExportedProgram:
    """
    :func:`export` takes any nn.Module along with example inputs, and produces a traced graph representing
    only the Tensor computation of the function in an Ahead-of-Time (AOT) fashion,
    which can subsequently be executed with different inputs or serialized.  The
    traced graph (1) produces normalized operators in the functional ATen operator set
    (as well as any user-specified custom operators), (2) has eliminated all Python control
    flow and data structures (with certain exceptions), and (3) records the set of
    shape constraints needed to show that this normalization and control-flow elimination
    is sound for future inputs.

    **Soundness Guarantee**

    While tracing, :func:`export()` takes note of shape-related assumptions
    made by the user program and the underlying PyTorch operator kernels.
    The output :class:`ExportedProgram` is considered valid only when these
    assumptions hold true.

    Tracing makes assumptions on the shapes (not values) of input tensors.
    Such assumptions must be validated at graph capture time for :func:`export`
    to succeed. Specifically:

    - Assumptions on static shapes of input tensors are automatically validated without additional effort.
    - Assumptions on dynamic shape of input tensors require explicit specification
      by using the :func:`Dim` API to construct dynamic dimensions and by associating
      them with example inputs through the ``dynamic_shapes`` argument.

    If any assumption can not be validated, a fatal error will be raised. When that happens,
    the error message will include suggested fixes to the specification that are needed
    to validate the assumptions. For example :func:`export` might suggest the
    following fix to the definition of a dynamic dimension ``dim0_x``, say appearing in the
    shape associated with input ``x``, that was previously defined as ``Dim("dim0_x")``::

        dim = Dim("dim0_x", max=5)

    This example means the generated code requires dimension 0 of input ``x`` to be less
    than or equal to 5 to be valid. You can inspect the suggested fixes to dynamic dimension
    definitions and then copy them verbatim into your code without needing to change the
    ``dynamic_shapes`` argument to your :func:`export` call.

    Args:
        mod: We will trace the forward method of this module.

        args: Example positional inputs.

        kwargs: Optional example keyword inputs.

        dynamic_shapes:
         An optional argument where the type should either be:
         1) a dict from argument names of ``f`` to their dynamic shape specifications,
         2) a tuple that specifies dynamic shape specifications for each input in original order.
         If you are specifying dynamism on keyword args, you will need to pass them in the order that
         is defined in the original function signature.

         The dynamic shape of a tensor argument can be specified as either
         (1) a dict from dynamic dimension indices to :func:`Dim` types, where it is
         not required to include static dimension indices in this dict, but when they are,
         they should be mapped to None; or (2) a tuple / list of :func:`Dim` types or None,
         where the :func:`Dim` types correspond to dynamic dimensions, and static dimensions
         are denoted by None. Arguments that are dicts or tuples / lists of tensors are
         recursively specified by using mappings or sequences of contained specifications.

        strict: When disabled (default), the export function will trace the program through
         Python runtime, which by itself will not validate some of the implicit assumptions
         baked into the graph. It will still validate most critical assumptions like shape
         safety. When enabled (by setting ``strict=True``), the export function will trace
         the program through TorchDynamo which will ensure the soundness of the resulting
         graph. TorchDynamo has limited Python feature coverage, thus you may experience more
         errors. Note that toggling this argument does not affect the resulting IR spec to be
         different and the model will be serialized in the same way regardless of what value
         is passed here.

        preserve_module_call_signature: A list of submodule paths for which the original
         calling conventions are preserved as metadata. The metadata will be used when calling
         torch.export.unflatten to preserve the original calling conventions of modules.

    Returns:
        An :class:`ExportedProgram` containing the traced callable.

    **Acceptable input/output types**

    Acceptable types of inputs (for ``args`` and ``kwargs``) and outputs include:

    - Primitive types, i.e. ``torch.Tensor``, ``int``, ``float``, ``bool`` and ``str``.
    - Dataclasses, but they must be registered by calling :func:`register_dataclass` first.
    - (Nested) Data structures comprising of ``dict``, ``list``, ``tuple``, ``namedtuple`` and
      ``OrderedDict`` containing all above types.

    """
    from ._trace import _export

    if not isinstance(mod, torch.nn.Module):
        raise ValueError(
            f"Expected `mod` to be an instance of `torch.nn.Module`, got {type(mod)}."
        )
    if isinstance(mod, torch.jit.ScriptModule):
        raise ValueError(
            "Exporting a ScriptModule is not supported. "
            "Maybe try converting your ScriptModule to an ExportedProgram "
            "using `TS2EPConverter(mod, args, kwargs).convert()` instead."
        )

    try:
        return _export(
            mod,
            args,
            kwargs,
            dynamic_shapes,
            strict=strict,
            preserve_module_call_signature=preserve_module_call_signature,
            pre_dispatch=True,
        )
    except Exception as e:
        draft_export_msg = (
            "The error above occurred when calling torch.export.export. If you would "
            "like to view some more information about this error, and get a list "
            "of all other errors that may occur in your export call, you can "
            "replace your `export()` call with `draft_export()`."
        )

        # For errors that we know can be caught by draft-export, add the message
        # to ask users to try out draft-export
        if isinstance(
            e,
            (
                torch.fx.experimental.symbolic_shapes.GuardOnDataDependentSymNode,
                torch._subclasses.fake_tensor.UnsupportedOperatorException,
                torch._dynamo.exc.UserError,
                torch.fx.experimental.symbolic_shapes.ConstraintViolationError,
            ),
        ):
            new_msg = str(e) + "\n\n" + draft_export_msg
            e.args = (new_msg,)
        elif isinstance(e, RuntimeError) and "no fake impl registered" in str(e):
            new_msg = str(e) + "\n\n" + draft_export_msg
            e.args = (new_msg,)
        raise e
