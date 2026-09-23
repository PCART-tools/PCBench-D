def _pack_msg(job_id: int, length: int) -> bytes:
    return struct.pack("nn", job_id, length)
