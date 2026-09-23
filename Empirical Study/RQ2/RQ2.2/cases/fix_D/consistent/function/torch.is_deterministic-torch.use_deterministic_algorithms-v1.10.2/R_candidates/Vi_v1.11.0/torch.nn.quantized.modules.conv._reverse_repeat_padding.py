def _reverse_repeat_padding(padding: List[int]) -> List[int]:
    _reversed_padding_repeated_twice: List[int] = []
    N = len(padding)
    for idx in range(N):
        for _ in range(2):
            _reversed_padding_repeated_twice.append(padding[N - idx - 1])
    return _reversed_padding_repeated_twice
