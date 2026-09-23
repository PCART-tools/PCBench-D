def _send_msg(write_pipe: IO[bytes], job_id: int, job_data: bytes = b"") -> None:
    length = len(job_data)
    write_pipe.write(_pack_msg(job_id, length))
    if length > 0:
        write_pipe.write(job_data)
    write_pipe.flush()
