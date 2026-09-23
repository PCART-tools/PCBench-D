@contextmanager
def decompose(
    decomposition_table: Optional[Mapping[OpOverload, Callable]],
) -> Generator[Mapping[OpOverload, Callable], None, None]:
    global CURRENT_DECOMPOSITION_TABLE
    old_decomposition_table = CURRENT_DECOMPOSITION_TABLE
    CURRENT_DECOMPOSITION_TABLE = decomposition_table or {}
    try:
        yield CURRENT_DECOMPOSITION_TABLE
    finally:
        CURRENT_DECOMPOSITION_TABLE = old_decomposition_table
