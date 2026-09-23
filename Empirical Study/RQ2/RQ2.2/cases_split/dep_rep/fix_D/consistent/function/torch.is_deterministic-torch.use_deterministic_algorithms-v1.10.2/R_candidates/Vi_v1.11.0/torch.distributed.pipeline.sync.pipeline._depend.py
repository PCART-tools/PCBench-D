def _depend(fork_from: Batch, join_to: Batch) -> None:
    fork_from_idx = fork_from.find_tensor_idx()
    join_to_idx = join_to.find_tensor_idx()

    fork_from[fork_from_idx], phony = fork(fork_from[fork_from_idx])
    join_to[join_to_idx] = join(join_to[join_to_idx], phony)
