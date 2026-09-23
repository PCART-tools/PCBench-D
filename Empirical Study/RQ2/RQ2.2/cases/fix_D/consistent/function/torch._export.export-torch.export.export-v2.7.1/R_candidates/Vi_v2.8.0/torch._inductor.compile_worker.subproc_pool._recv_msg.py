def _recv_msg(read_pipe: IO[bytes]) -> tuple[int, bytes]:
    job_id, length = _unpack_msg(read_pipe.read(msg_bytes))
    data = read_pipe.read(length) if length > 0 else b""
    return job_id, data
