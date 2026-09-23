def export_for_training(
    mod: torch.nn.Module,
    args: tuple[Any, ...],
    kwargs: Optional[dict[str, Any]] = None,
    *,
    dynamic_shapes: Optional[Union[dict[str, Any], tuple[Any], list[Any]]] = None,
    strict: bool = True,
    preserve_module_call_signature: tuple[str, ...] = (),
) -> ExportedProgram:
    """
    :func:`export_for_training` takes any nn.Module along with example inputs, and produces a traced graph representing
    only the Tensor computation of the function in an Ahead-of-Time (AOT) fashion,
    which can subsequently be executed with different inputs or serialized. The
    traced graph (1) produces normalized operators in the all ATen operator set
    (as well as any user-specified custom operators), (2) has eliminated all Python control
    flow and data structures (with certain exceptions), and (3) records the set of
    shape constraints needed to show that this normalization and control-flow elimination
    is sound for future inputs. This API is intended for PT2 quantization training use cases
    and will soon be the default IR of torch.export.export in the near future. To read further about
    the motivation behind this change, please refer to
    https://dev-discuss.pytorch.org/t/why-pytorch-does-not-need-a-new-standardized-operator-set/2206
    With this API, and :func:`run_decompositions()`, you should be able to get inference IR with
    your custom decomposition behaviour.

    **Soundness Guarantee**

    See :func:`export()` docstring for more details.

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

        strict: When enabled (default), the export function will trace the program through
         TorchDynamo which will ensure the soundness of the resulting graph. Otherwise, the
         exported program will not validate the implicit assumptions baked into the graph and
         may cause behavior divergence between the original model and the exported one. This is
         useful when users need to workaround bugs in the tracer, or simply want incrementally
         enable safety in their models. Note that this does not affect the resulting IR spec
         to be different and the model will be serialized in the same way regardless of what value
         is passed here.
         WARNING: This option is experimental and use this at your own risk.

    Returns:
        An :class:`ExportedProgram` containing the traced callable.

    **Acceptable input/output types**

    Acceptable types of inputs (for ``args`` and ``kwargs``) and outputs include:

    - Primitive types, i.e. ``torch.Tensor``, ``int``, ``float``, ``bool`` and ``str``.
    - Dataclasses, but they must be registered by calling :func:`register_dataclass` first.
    - (Nested) Data structures comprising of ``dict``, ``list``, ``tuple``, ``namedtuple`` and
      ``OrderedDict`` containing all above types.

    """
    from ._trace import _export_for_training

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
    return _export_for_training(
        mod,
        args,
        kwargs,
        dynamic_shapes,
        strict=strict,
        preserve_module_call_signature=preserve_module_call_signature,
    )
