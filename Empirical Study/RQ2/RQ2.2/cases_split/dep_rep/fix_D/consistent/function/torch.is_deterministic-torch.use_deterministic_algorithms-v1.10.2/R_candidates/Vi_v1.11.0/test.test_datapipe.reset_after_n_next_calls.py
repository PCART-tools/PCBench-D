def reset_after_n_next_calls(datapipe: Union[IterDataPipe[T_co], MapDataPipe[T_co]],
                             n: int) -> Tuple[List[T_co], List[T_co]]:
    """
    Given a DataPipe and integer n, iterate the DataPipe for n elements and store the elements into a list
    Then, reset the DataPipe and return a tuple of two lists
        1. A list of elements yielded before the reset
        2. A list of all elements of the DataPipe after the reset
    """
    it = iter(datapipe)
    res_before_reset = []
    for _ in range(n):
        res_before_reset.append(next(it))
    return res_before_reset, list(datapipe)
