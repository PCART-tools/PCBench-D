def _fatal_signal_function(expected_error_index: int, sig: int):
    rank = int(os.environ["RANK"])
    if rank == expected_error_index:
        os.kill(os.getpid(), sig)
