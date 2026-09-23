def trace(
    func,
    example_inputs,
    optimize=None,
    check_trace=True,
    check_inputs=None,
    check_tolerance=1e-5,
    strict=True,
    _force_outplace=False,
    _module_class=None,
    _compilation_unit=_python_cu,
):
    """
    Trace a function and return an executable  or :class:`ScriptFunction`
    that will be optimized using just-in-time compilation. Tracing is ideal for
    code that operates only on ``Tensor``\\s and lists, dictionaries, and
    tuples of ``Tensor``\\s.

    Using `torch.jit.trace` and `torch.jit.trace_module`, you can turn an
    existing module or Python function into a TorchScript
    :class:`ScriptFunction` or :class:`ScriptModule`. You must provide example
    inputs, and we run the function, recording the operations performed on all
    the tensors.

    * The resulting recording of a standalone function produces `ScriptFunction`.
    * The resulting recording of `nn.Module.forward` or `nn.Module` produces
      `ScriptModule`.

    This module also contains any parameters that the original
    module had as well.

    Warning:
        Tracing only correctly records functions and modules which are not data
        dependent (e.g., do not have conditionals on data in tensors) and do not have
        any untracked external dependencies (e.g., perform input/output or
        access global variables). Tracing only records operations done when the given
        function is run on the given tensors. Therefore, the returned
        `ScriptModule` will always run the same traced graph on any input. This
        has some important implications when your module is expected to run
        different sets of operations, depending on the input and/or the module
        state. For example,

        * Tracing will not record any control-flow like if-statements or loops.
          When this control-flow is constant across your module, this is fine
          and it often inlines the control-flow decisions. But sometimes the
          control-flow is actually part of the model itself. For instance, a
          recurrent network is a loop over the (possibly dynamic) length of an
          input sequence.
        * In the returned :class:`ScriptModule`, operations that have different
          behaviors in ``training`` and ``eval`` modes will always behave as if
          it is in the mode it was in during tracing, no matter which mode the
          `ScriptModule` is in.

        In cases like these, tracing would not be appropriate and
        :func:`scripting <torch.jit.script>` is a better choice. If you trace
        such models, you may silently get incorrect results on subsequent
        invocations of the model. The tracer will try to emit warnings when
        doing something that may cause an incorrect trace to be produced.

    Args:
        func (callable or torch.nn.Module):  A Python function or `torch.nn.Module`
            that will be run with `example_inputs`. `func` arguments and return
            values  must be tensors or (possibly nested) tuples that contain
            tensors. When a module is passed `torch.jit.trace`, only the
            ``forward`` method is run and traced (see :func:`torch.jit.trace
            <torch.jit.trace_module>` for details).
        example_inputs (tuple or torch.Tensor):  A tuple of example inputs that
            will be passed to the function while tracing. The resulting trace
            can be run with inputs of different types and shapes assuming the
            traced operations support those types and shapes. `example_inputs`
            may also be a single Tensor in which case it is automatically
            wrapped in a tuple.

    Keyword arguments:
        check_trace (``bool``, optional): Check if the same inputs run through
            traced code produce the same outputs. Default: ``True``. You might want
            to disable this if, for example, your network contains non-
            deterministic ops or if you are sure that the network is correct despite
            a checker failure.

        check_inputs (list of tuples, optional): A list of tuples of input
            arguments that should be used to check the trace against what is
            expected. Each tuple is equivalent to a set of input arguments that
            would be specified in ``example_inputs``. For best results, pass in
            a set of checking inputs representative of the space of shapes and
            types of inputs you expect the network to see.  If not specified,
            the original ``example_inputs`` are used for checking
        check_tolerance (float, optional): Floating-point comparison tolerance
            to use in the checker procedure.  This can be used to relax the
            checker strictness in the event that results diverge numerically
            for a known reason, such as operator fusion.
        strict (``bool``, optional): run the tracer in a strict mode or not
            (default: ``True``). Only turn this off when you want the tracer to
            record your mutable container types (currently ``list``/``dict``)
            and you are sure that the container you are using in your
            problem is a ``constant`` structure and does not get used as
            control flow (if, for) conditions.

    Returns:
        If `func` is `nn.Module` or ``forward`` of `nn.Module`, `trace` returns
        a :class:`ScriptModule` object with a single ``forward`` method
        containing the traced code.  The returned `ScriptModule` will
        have the same set of sub-modules and parameters as the original
        ``nn.Module``.  If ``func`` is a standalone function, ``trace``
        returns `ScriptFunction`.

    Example (tracing a function):

    .. testcode::

        import torch

        def foo(x, y):
            return 2 * x + y

        # Run `foo` with the provided inputs and record the tensor operations
        traced_foo = torch.jit.trace(foo, (torch.rand(3), torch.rand(3)))

        # `traced_foo` can now be run with the TorchScript interpreter or saved
        # and loaded in a Python-free environment

    Example (tracing an existing module)::

        import torch
        import torch.nn as nn

        class Net(nn.Module):
            def __init__(self):
                super(Net, self).__init__()
                self.conv = nn.Conv2d(1, 1, 3)

            def forward(self, x):
                return self.conv(x)

        n = Net()
        example_weight = torch.rand(1, 1, 3, 3)
        example_forward_input = torch.rand(1, 1, 3, 3)

        # Trace a specific method and construct `ScriptModule` with
        # a single `forward` method
        module = torch.jit.trace(n.forward, example_forward_input)

        # Trace a module (implicitly traces `forward`) and construct a
        # `ScriptModule` with a single `forward` method
        module = torch.jit.trace(n, example_forward_input)

    """
    if not _enabled:
        return func
    if optimize is not None:
        warnings.warn(
            "`optimize` is deprecated and has no effect. Use `with torch.jit.optimized_execution() instead"
        )

    if isinstance(func, torch.jit.ScriptModule):
        # it is hard to trace it because the forward method on ScriptModule is already defined, so it
        # would result in an error.
        warnings.warn(
            "The input to trace is already a ScriptModule, tracing it is a no-op. Returning the object as is."
        )
        return func

    if isinstance(func, torch.nn.Module):
        return trace_module(
            func,
            {"forward": example_inputs},
            None,
            check_trace,
            wrap_check_inputs(check_inputs),
            check_tolerance,
            strict,
            _force_outplace,
            _module_class,
        )

    if (
        hasattr(func, "__self__")
        and isinstance(func.__self__, torch.nn.Module)
        and func.__name__ == "forward"
    ):
        return trace_module(
            func.__self__,
            {"forward": example_inputs},
            None,
            check_trace,
            wrap_check_inputs(check_inputs),
            check_tolerance,
            strict,
            _force_outplace,
            _module_class,
        )

    # Special case for common case of passing a single Tensor
    if isinstance(example_inputs, (torch.Tensor, dict)):
        example_inputs = (example_inputs,)
    # done primarily so that weird iterables fail here and not pybind11 code
    elif not isinstance(example_inputs, tuple):
        example_inputs = tuple(example_inputs)

    var_lookup_fn = _create_interpreter_name_lookup_fn(0)

    if hasattr(func, "__self__") and isinstance(func.__self__, torch.nn.Module):
        raise AttributeError(
            "trace doesn't support compiling individual module's functions.\n"
            "Please use trace_module"
        )

    name = _qualified_name(func)
    traced = torch._C._create_function_from_trace(
        name,
        func,
        example_inputs,
        var_lookup_fn,
        strict,
        _force_outplace,
        get_callable_argument_names(func)
    )

    # Check the trace against new traces created from user-specified inputs
    if check_trace:
        if check_inputs is not None:
            _check_trace(
                check_inputs,
                func,
                traced,
                check_tolerance,
                strict,
                _force_outplace,
                False,
                _module_class,
            )
        else:
            _check_trace(
                [example_inputs],
                func,
                traced,
                check_tolerance,
                strict,
                _force_outplace,
                False,
                _module_class,
            )

    return traced
