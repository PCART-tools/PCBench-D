@lru_cache(None)
def uninteresting_files() -> set[str]:
    import torch._compile
    import torch._dynamo.eval_frame
    import torch._inductor.sizevars
    import torch._library.custom_ops
    import torch._library.fake_impl
    import torch._logging
    import torch._subclasses.fake_tensor
    import torch._subclasses.meta_utils

    mods = [
        sys.modules[__name__],
        torch.fx.experimental.recording,
        torch.fx.experimental.sym_node,
        torch.fx.interpreter,
        torch,
        torch._compile,
        torch._dynamo.eval_frame,
        torch._inductor.sizevars,
        torch._library.custom_ops,
        torch._library.fake_impl,
        torch._subclasses.meta_utils,
        torch._subclasses.fake_tensor,
        torch._logging._internal,
        torch._logging.structured,
    ]
    import torch._dynamo.guards

    return (
        {inspect.getfile(m) for m in mods}
        | torch._dynamo.guards.uninteresting_files()
        | {"<string>"}
    )
