def _checkpoint_without_reentrant(function, preserve_rng_state=True, *args):
    """Checkpointining without re-entrant autograd
    Args:
        function: describes what to run in the forward pass of the model or
            part of the model. It should also know how to handle the inputs
            passed as the tuple. For example, in LSTM, if user passes
            ``(activation, hidden)``, :attr:`function` should correctly use the
            first input as ``activation`` and the second input as ``hidden``
        preserve_rng_state(bool, optional, default=True):  Omit stashing and restoring
            the RNG state during each checkpoint.
        *args: Arguments to pass in to the given ``function``.
    """
    had_autocast_in_fwd = torch.is_autocast_enabled()

    if preserve_rng_state:
        fwd_cpu_state = torch.get_rng_state()
        # Don't eagerly initialize the cuda context by accident.
        # (If the user intends that the context is initialized later, within their
        # run_function, we SHOULD actually stash the cuda state here.  Unfortunately,
        # we have no way to anticipate this will happen before we run the function.
        # If they do so, we raise an error.)
        had_cuda_in_fwd = False
        if torch.cuda._initialized:
            had_cuda_in_fwd = True
            fwd_gpu_devices, fwd_gpu_states = get_device_states(*args)

    storage: List[Union[torch.Tensor, None]] = []
    counter = 0

    def pack(x):
        nonlocal counter
        counter += 1
        # TODO(varal7): Instead of returning indices, we can return things metadata (such as
        # size, device, ...) to catch certain cases of undeterministic behavior of the forward
        return counter - 1

    def unpack(x):
        if len(storage) == 0:

            def inner_pack(inner):
                storage.append(inner)
                return None

            def inner_unpack(packed):
                raise RuntimeError("You are calling backwards on a tensor that is never exposed. Please open an issue.")

            # Stash the surrounding rng state, and mimic the state that was
            # present at this time during forward.  Restore the surrounding state
            # when we're done.
            rng_devices = []
            if preserve_rng_state and had_cuda_in_fwd:
                rng_devices = fwd_gpu_devices
            with torch.random.fork_rng(devices=rng_devices, enabled=preserve_rng_state):
                if preserve_rng_state:
                    torch.set_rng_state(fwd_cpu_state)
                    if had_cuda_in_fwd:
                        set_device_states(fwd_gpu_devices, fwd_gpu_states)
                with torch.enable_grad(), torch.cuda.amp.autocast(had_autocast_in_fwd):
                    with torch.autograd.graph.saved_tensors_hooks(inner_pack, inner_unpack):
                        _unused = function(*args)

        return storage[x]

    with torch.autograd.graph.saved_tensors_hooks(pack, unpack):
        output = function(*args)
        if torch.cuda._initialized and not had_cuda_in_fwd:
            # Cuda was not initialized before running the forward, so we didn't
            # stash the CUDA state.
            raise RuntimeError(
                "PyTorch's CUDA state was initialized in the forward pass "
                "of a Checkpoint, which is not allowed. Please open an issue "
                "if you need this feature.")

    return output
