def analyze_memory_coalescing(
    fused_node: Union["FusedSchedulerNode", "SchedulerNode"],
) -> Optional[CoalesceVarAnalysis]:
    """
    Find variables that coalesce the reads and writes and score the total size.

    If uncoalesced memory expressions are found, look for additionally tiling of variables
    which will coalesce memory accesses.

    For instance - for the following expression:

    (32*p0) // 2048

    Tiling p0 by 64 will make this expression coalesced.
    """

    norm_read_writes = extract_normalized_read_writes(fused_node)

    if norm_read_writes is None:
        return None

    reads = norm_read_writes.reads
    writes = norm_read_writes.writes
    var_ranges = norm_read_writes.var_ranges

    coalesced_by_var: dict[sympy.Symbol, int] = Counter()
    uncoalesced_addrs: dict[sympy.Expr, int] = Counter()

    for is_read, (memory_expr, buf_names) in itertools.chain(
        ((True, item) for item in reads.items()),
        ((False, item) for item in writes.items()),
    ):
        # skip memory deps with indirect vars - todo: better handling
        indirect_expr = bool(
            memory_expr.free_symbols - norm_read_writes.var_ranges.keys()
        )

        if indirect_expr:
            continue

        size = get_score(memory_expr, var_ranges)
        if size == 0:
            continue

        maybe_coalesced_var = find_coalesced_var(memory_expr, var_ranges)

        byte_multipler = 0
        for buf_name in buf_names:
            if buf := V.graph.try_get_buffer(buf_name):
                byte_multipler += buf.dtype.itemsize

        # coalesced writes more important
        byte_multipler *= 1 if is_read else 2

        if maybe_coalesced_var:
            coalesced_by_var[maybe_coalesced_var] += size * byte_multipler
        else:
            uncoalesced_addrs[memory_expr] += size * byte_multipler

    if not uncoalesced_addrs:
        return CoalesceVarAnalysis(
            coalesced_by_var=coalesced_by_var, norm_read_writes=norm_read_writes
        )

    # map from var -> tiling -> total_score
    tiling_scores: dict[sympy.Expr, dict[int, int]] = defaultdict(Counter)

    for uncoalesced_expr, addr_score in uncoalesced_addrs.items():
        expr_subs = dict.fromkeys(uncoalesced_expr.free_symbols, 0)
        for v in uncoalesced_expr.free_symbols:
            # skip non iter/reduce var variables
            if v not in var_ranges:
                continue
            # skip small addrs
            if addr_score == 0:
                continue
            del expr_subs[v]
            single_var_expr = sympy_subs(uncoalesced_expr, expr_subs)
            expr_subs[v] = 0
            tiling_factor = solve_for_tiling(single_var_expr)
            if (
                tiling_factor is None
                or not tiling_factor.is_constant()
                or not tiling_factor.is_integer
            ):
                continue

            tiling_factor = int(tiling_factor)
            if not V.graph.sizevars.statically_known_lt(tiling_factor, var_ranges[v]):
                continue

            # TODO - if a var is in the middle, such as [n0, n1, n2]
            # n1 can can be split beyond range

            MIN_TILING_BLOCK = 8
            if not all(
                V.graph.sizevars.statically_known_lt(MIN_TILING_BLOCK, block)
                for block in (tiling_factor, var_ranges[v] // tiling_factor)
            ):
                continue

            tiling_scores[v][tiling_factor] += addr_score

    if len(tiling_scores) == 0:
        return CoalesceVarAnalysis(
            coalesced_by_var=coalesced_by_var, norm_read_writes=norm_read_writes
        )

    best_tiling: Optional[tuple[sympy.Expr, int]] = None
    best_tiling_score = 0

    for var, tiling_counter in tiling_scores.items():
        for tile, tile_score in tiling_counter.items():
            if tile_score > best_tiling_score:
                best_tiling = (var, tile)
                best_tiling_score = tile_score

    if best_tiling is None:
        return CoalesceVarAnalysis(
            coalesced_by_var=coalesced_by_var, norm_read_writes=norm_read_writes
        )

    # TODO - for strictly pointwise fusions,
    # we can consider just swizzling the var if the var we are going to tile
    # does not coalesce a significant portion of global reads
    # TODO - could also prefer index var splits to reduction, better tested
    return CoalesceVarAnalysis(
        coalesced_by_var=coalesced_by_var,
        norm_read_writes=norm_read_writes,
        suggested_split=VarTiling(best_tiling[0], best_tiling[1], best_tiling_score),
    )
