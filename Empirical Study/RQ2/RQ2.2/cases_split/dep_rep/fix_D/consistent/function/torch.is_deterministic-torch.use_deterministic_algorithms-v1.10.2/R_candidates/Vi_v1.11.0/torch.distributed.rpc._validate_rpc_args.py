    def _validate_rpc_args(backend, store, name, rank, world_size, rpc_backend_options):
        type_mapping = {
            backend: backend_registry.BackendType,
            store: dist.Store,
            name: str,
            rank: numbers.Integral,
            world_size: numbers.Integral,
            rpc_backend_options: RpcBackendOptions,
        }
        for arg, arg_type in type_mapping.items():
            if not isinstance(arg, arg_type):
                raise RuntimeError(
                    "Argument {} must be of type {} but got type {}".format(
                        arg, arg_type, type(arg)
                    )
                )
