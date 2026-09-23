def checkpoint(function: Function, input):
    """Makes a checkpoint with a simple interface like
    :func:`torch.utils.checkpoint.checkpoint`. It's only used to test or debug
    :class:`Checkpoint` and :class:`Recompute` without boilerplate.
    """
    batch = Batch(input)

    chk = Checkpointing(function, batch)
    batch = chk.checkpoint()
    chk.recompute(batch)

    return batch.values
