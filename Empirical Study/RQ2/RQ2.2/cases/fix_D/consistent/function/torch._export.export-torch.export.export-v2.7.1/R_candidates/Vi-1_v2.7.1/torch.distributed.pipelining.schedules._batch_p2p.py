def _batch_p2p(p2p_ops: list[dist.P2POp], desc: Optional[str] = None):
    """
    Simple wrapper over batch_isend_irecv from torch.distributed, which just adds a descriptive logger on top.
    """
    if len(p2p_ops) == 0:
        return None
    desc_str = f"{desc}, " if desc else ""
    logger.debug("batch_p2p %s%s", desc_str, p2p_ops)
    return dist.batch_isend_irecv(p2p_ops).pop()
