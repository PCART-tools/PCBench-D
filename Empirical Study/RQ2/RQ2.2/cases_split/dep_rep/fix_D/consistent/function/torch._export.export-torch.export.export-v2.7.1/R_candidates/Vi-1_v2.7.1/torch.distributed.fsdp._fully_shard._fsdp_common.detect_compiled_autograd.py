    def detect_compiled_autograd():
        assert not torch.compiler.is_compiling(), (
            "`detect_compiled_autograd()` is designed to be called in eager mode"
        )
        global _compiled_autograd_enabled
        import torch._dynamo.compiled_autograd as ca

        _compiled_autograd_enabled = (
            ca.compiled_autograd_enabled
            or ca.compiled_autograd_enabled_force_eager
            or ca.in_compiled_autograd_region
        )
