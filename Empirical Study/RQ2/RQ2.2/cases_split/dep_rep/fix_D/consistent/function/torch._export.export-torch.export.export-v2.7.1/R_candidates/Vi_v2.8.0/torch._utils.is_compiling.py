    def is_compiling() -> bool:
        """
        Indicates whether we are tracing/compiling with torch.compile() or torch.export().
        """
        warnings.warn(  # use `warnings.warn` instead of `@deprecated`
            "`torch._utils.is_compiling` is deprecated. Use `torch.compiler.is_compiling` instead.",
            # FutureWarning,  # TorchScript does not support Warning type
            stacklevel=2,
        )
        return torch.compiler.is_compiling()
