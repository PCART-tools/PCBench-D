    def is_compiling() -> bool:
        """
        Indicates whether we are tracing/compiling with torch.compile() or torch.export().
        """
        # NOTE: With `@torch.compile(backend="eager")`, torch._dynamo.is_compiling() will get traced
        # and return true. torch.compiler.is_compiling() is skipped and will return false.
        return torch.compiler.is_compiling()
