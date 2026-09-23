def _unpack_msg(data: bytes) -> tuple[int, int]:
    if not data:
        return -1, -1
    return struct.unpack("nn", data)
