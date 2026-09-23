    def init_rpc(
        name,
        backend=None,
        rank=-1,
        world_size=None,
        rpc_backend_options=None,
    ):
        r"""
        Initializes RPC primitives such as the local RPC agent
        and distributed autograd, which immediately makes the current
        process ready to send and receive RPCs.

        Args:
            name (str): a globally unique name of this node. (e.g.,
                ``Trainer3``, ``ParameterServer2``, ``Master``, ``Worker1``)
                Name can only contain number, alphabet, underscore, colon,
                and/or dash, and must be shorter than 128 characters.
            backend (BackendType, optional): The type of RPC backend
                implementation. Supported values is
                ``BackendType.TENSORPIPE`` (the default).
                See :ref:`rpc-backends` for more information.
            rank (int): a globally unique id/rank of this node.
            world_size (int): The number of workers in the group.
            rpc_backend_options (RpcBackendOptions, optional): The options
                passed to the RpcAgent constructor. It must be an agent-specific
                subclass of :class:`~torch.distributed.rpc.RpcBackendOptions`
                and contains agent-specific initialization configurations. By
                default, for all agents, it sets the default timeout to 60
                seconds and performs the rendezvous with an underlying process
                group initialized using ``init_method = "env://"``,
                meaning that environment variables ``MASTER_ADDR`` and
                ``MASTER_PORT`` need to be set properly. See
                :ref:`rpc-backends` for more information and find which options
                are available.
        """

        if backend is not None and not isinstance(
            backend, backend_registry.BackendType
        ):
            raise TypeError("Argument backend must be a member of BackendType")

        if rpc_backend_options is not None and not isinstance(
            rpc_backend_options, RpcBackendOptions
        ):
            raise TypeError(
                "Argument rpc_backend_options must be an instance of RpcBackendOptions"
            )

        # Try to detect the backend from the options
        if backend is None and rpc_backend_options is not None:
            for candidate_backend in BackendType:
                if isinstance(
                    rpc_backend_options,
                    type(
                        backend_registry.construct_rpc_backend_options(
                            candidate_backend
                        )
                    ),
                ):
                    backend = candidate_backend
                    break
            else:
                raise TypeError(
                    f"Could not infer backend for options {rpc_backend_options}"
                )
            # Ignore type error because mypy doesn't handle dynamically generated type objects (#4865)
            if backend != BackendType.TENSORPIPE:  # type: ignore[attr-defined]
                logger.warning(
                    f"RPC was initialized with no explicit backend but with options "  # type: ignore[attr-defined]
                    f"corresponding to {backend}, hence that backend will be used "
                    f"instead of the default {BackendType.TENSORPIPE}. To silence this "
                    f"warning pass `backend={backend}` explicitly."
                )

        if backend is None:
            backend = BackendType.TENSORPIPE  # type: ignore[attr-defined]

        if backend == BackendType.PROCESS_GROUP:  # type: ignore[attr-defined]
            raise RuntimeError(
                "RPC was initialized with the PROCESS_GROUP backend which has "
                "been removed and is superseded by the TENSORPIPE backend. "
                "Please migrate to the TENSORPIPE backend. "
                "PyTorch v1.9 was the last release that carries PROCESS_GROUP "
                "RPC backend."
            )

        if rpc_backend_options is None:
            # default construct a set of RPC backend options.
            rpc_backend_options = backend_registry.construct_rpc_backend_options(
                backend
            )

        # Rendezvous.
        # This rendezvous state sometimes is destroyed before all processes
        # finishing handshaking. To avoid that issue, we make it global to
        # keep it alive.
        global rendezvous_iterator
        rendezvous_iterator = torch.distributed.rendezvous(
            rpc_backend_options.init_method, rank=rank, world_size=world_size
        )
        store, _, _ = next(rendezvous_iterator)

        # Use a PrefixStore to distinguish multiple invocations.
        with _init_counter_lock:
            global _init_counter
            store = dist.PrefixStore(str("rpc_prefix_{}".format(_init_counter)), store)
            _init_counter += 1

        # Initialize autograd before RPC since _init_rpc_backend guarantees all
        # processes sync via the store. If we initialize autograd after RPC,
        # there could be a race where some nodes might have initialized autograd
        # and others might not have. As a result, a node calling
        # torch.distributed.autograd.backward() would run into errors since
        # other nodes might not have been initialized.
        dist_autograd._init(rank)

        _set_profiler_node_id(rank)
        # Initialize RPC.
        _init_rpc_backend(backend, store, name, rank, world_size, rpc_backend_options)
