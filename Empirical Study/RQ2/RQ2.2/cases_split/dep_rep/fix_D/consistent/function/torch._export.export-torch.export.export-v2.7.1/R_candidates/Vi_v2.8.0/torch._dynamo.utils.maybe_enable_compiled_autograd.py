@contextlib.contextmanager
def maybe_enable_compiled_autograd(should_enable, fullgraph=True, dynamic=True):
    if not should_enable:
        yield
    else:

        def compiler_fn(gm):
            def inner_compiler(gm_, example_inputs_):
                torch._dynamo.utils.counters["compiled_autograd"]["compiles"] += 1
                return torch._inductor.compile(gm_, example_inputs_)

            return torch.compile(
                gm, backend=inner_compiler, fullgraph=fullgraph, dynamic=dynamic
            )

        with torch._dynamo.compiled_autograd._enable(compiler_fn) as ctx:
            yield ctx
