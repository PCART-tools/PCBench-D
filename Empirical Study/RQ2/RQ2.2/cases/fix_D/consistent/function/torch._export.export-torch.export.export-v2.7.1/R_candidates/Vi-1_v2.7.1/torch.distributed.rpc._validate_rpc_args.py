    def _validate_rpc_args(backend, store, name, rank, world_size, rpc_backend_options):
        type_mapping = {
            backend: backend_registry.BackendType,
            store: dist.Store,
            name: str,
            rank: numbers.Integral,
            # world_size can be None for a dynamic group
            world_size: (numbers.Integral, type(None)),
            rpc_backend_options: RpcBackendOptions,
        }
        for arg, arg_type in type_mapping.items():
            if not isinstance(arg, arg_type):  # type: ignore[arg-type]
                raise RuntimeError(
                    f"Argument {arg} must be of type {arg_type} but got type {type(arg)}"
                )
