        def GPUTarget(
            backend: str,
            arch: Union[int, str],
            warp_size: int,
        ) -> Any:
            if torch.version.hip:
                return [backend, arch, warp_size]
            return (backend, arch)
