def run_node(tracer, node, args, kwargs, nnmodule):
    """
    Runs a given node, with the given args and kwargs.

    Behavior is dictated by a node's op.

    run_node is useful for extracting real values out of nodes.
    See get_real_value for more info on common usage.

    Note: The tracer arg is only used for 'get_attr' ops
    Note: The nnmodule arg is only used for 'call_module' ops

    Nodes that are not call_function, call_method, call_module, or get_attr will
    raise an AssertionError.
    """
    op = node.op

    with set_current_node(node):

        def make_error_message(e):
            return (
                f"Dynamo failed to run FX node with fake tensors: {op} {node.target}(*{args}, **{kwargs}): got "
                + repr(e)
            )

        from .exc import Unsupported

        try:
            if op == "call_function":
                return node.target(*args, **kwargs)
            elif op == "call_method":
                if not hasattr(args[0], node.target):
                    from .exc import unimplemented_v2

                    unimplemented_v2(
                        gb_type="Missing attribute when running call_method node",
                        context="",
                        explanation=make_error_message("attribute not defined"),
                        hints=[],
                    )
                return getattr(args[0], node.target)(*args[1:], **kwargs)
            elif op == "call_module":
                assert nnmodule is not None
                return nnmodule(*args, **kwargs)
            elif op == "get_attr":
                return tracer.output_graph.get_submodule(node.target)
            elif op == "placeholder":
                assert "example_value" in node.meta
                return node.meta["example_value"]

        except (NotImplementedError, UnsupportedFakeTensorException) as e:
            # NB: mimic how wrap_fake_exception does it
            from .exc import unimplemented_v2

            hints = []
            if isinstance(e, NotImplementedError):
                hints = [
                    "If the op is a PyTorch op, please file an issue to PyTorch.",
                ]

            unimplemented_v2(
                gb_type="NotImplementedError/UnsupportedFakeTensorException when running FX node",
                context="",
                explanation=make_error_message(e),
                hints=hints,
                from_exc=e,
            )
        except Unsupported:
            raise
        except Exception as e:
            raise RuntimeError(make_error_message(e)).with_traceback(
                e.__traceback__
            ) from e

    raise AssertionError(op)
