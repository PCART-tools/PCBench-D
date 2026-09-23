def remove_identity(gm: torch.fx.GraphModule) -> torch.fx.GraphModule:
    """
    Removes all identity layers from the module.
    """

    class IdentityRemover(torch.fx.Transformer):
        def call_module(self, target, args, kwargs):
            if isinstance(self.submodules[target], nn.Identity):
                assert len(args) == 1
                return args[0]
            else:
                return super().call_module(target, args, kwargs)

    return IdentityRemover(gm).transform()
