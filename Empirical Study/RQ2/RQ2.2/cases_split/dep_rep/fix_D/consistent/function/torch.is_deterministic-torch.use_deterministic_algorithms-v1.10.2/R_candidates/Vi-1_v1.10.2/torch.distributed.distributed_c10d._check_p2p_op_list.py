def _check_p2p_op_list(p2p_op_list):
    """
    Helper to check that the ``p2p_op_list`` is a list of P2POp instances and
    all ops use the same backend.
    """
    if not isinstance(p2p_op_list, list) or not all(
        isinstance(p2p_op, P2POp) for p2p_op in p2p_op_list
    ):
        raise RuntimeError(
            "Invalid ``p2p_op_list``. Each op is expected to "
            "to be of type ``torch.distributed.P2POp``."
        )

    backend = get_backend(p2p_op_list[0].group)
    if not all(backend == get_backend(p2p_op.group) for p2p_op in p2p_op_list):
        raise RuntimeError("All groups need to use the same backend.")
