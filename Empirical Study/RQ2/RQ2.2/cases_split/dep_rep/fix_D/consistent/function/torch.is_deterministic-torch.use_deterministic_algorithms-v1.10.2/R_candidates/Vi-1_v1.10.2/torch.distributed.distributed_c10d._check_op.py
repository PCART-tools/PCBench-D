def _check_op(op):
    """
    Helper to check that the ``op`` is either isend or irecv.
    """
    if op not in [isend, irecv]:
        raise RuntimeError(
            "Invalid ``op``. Expected ``op`` "
            "to be of type ``torch.distributed.isend`` or "
            "``torch.distributed.irecv``."
        )
