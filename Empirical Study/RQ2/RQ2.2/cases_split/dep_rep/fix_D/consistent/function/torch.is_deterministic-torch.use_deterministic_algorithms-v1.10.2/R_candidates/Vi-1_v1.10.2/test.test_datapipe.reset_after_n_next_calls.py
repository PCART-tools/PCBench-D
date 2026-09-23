def reset_after_n_next_calls(datapipe: IterDataPipe[T_co], n: int) -> Tuple[List[T_co], List[T_co]]:
    it = iter(datapipe)
    res_before_reset = []
    for _ in range(n):
        res_before_reset.append(next(it))
    return res_before_reset, list(datapipe)
