def last_producer(ops, blob):
    for (i, op) in reversed(list(enumerate(ops))):
        if blob in op.output:
            return i
    raise ValueError("Failed to find last producer of blob, %s", blob)
