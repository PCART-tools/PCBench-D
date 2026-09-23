def _deregister_effectful_op(op: OpType):
    if op not in SIDE_EFFECTS:
        raise RuntimeError(f"Op {op} is not registered as effectful")

    del SIDE_EFFECTS[op]
