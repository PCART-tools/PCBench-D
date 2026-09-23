    def breakpoint(rank: int = 0, skip: int = 0):
        """
        Set a breakpoint, but only on a single rank.  All other ranks will wait for you to be
        done with the breakpoint before continuing.

        Args:
            rank (int): Which rank to break on.  Default: ``0``
            skip (int): Skip the first ``skip`` calls to this breakpoint. Default: ``0``.
        """
        if skip > 0:
            key = hash(str(traceback.format_exc()))
            counter = _breakpoint_cache.get(key, 0) + 1
            _breakpoint_cache[key] = counter
            if counter <= skip:
                log.warning("Skip the breakpoint, counter=%d", counter)
                return

        if get_rank() == rank:
            pdb = _DistributedPdb()
            pdb.message(
                "\n!!! ATTENTION !!!\n\n"
                f"Type 'up' to get to the frame that called dist.breakpoint(rank={rank})\n"
            )
            pdb.set_trace()
        # If Meta/Python keys are in the TLS, we want to make sure that we ignore them
        # and hit the (default) CPU/CUDA implementation of barrier.
        meta_in_tls = torch._C._meta_in_tls_dispatch_include()
        guard = torch._C._DisableTorchDispatch()  # type: ignore[attr-defined]
        torch._C._set_meta_in_tls_dispatch_include(False)
        try:
            barrier()
        finally:
            torch._C._set_meta_in_tls_dispatch_include(meta_in_tls)
            del guard
