def compute_assignments_dp(ranges_sorted, init_assignment, counter=None):
    ''' Compute assignment for blobs in 'ranges_sorted' on top of 'init_assignment'
        using dynamic programming + recursion.

        ranges_sorted: blobs sorted by 'used'
        init_assignment: assignment to start with, blobs in 'ranges_sorted' should
                         not be used in 'init_assignment'

        Using f(b, k, init) to represent the best assignment for blobs b[0:k]
        given initial assignment 'init', we have
            f(b, k, init) = f(b, j, init) +
                            find_best(b[j:k], f(b, j, init))
        where j is the index of the last best assignment that is independent of
        blob b[k - 1] (b[k - 1] is compatible with all assignments in
        f(b, j, init)), and find_best(b1, init1) gives the best assignment
        for blobs in 'b1' based on the initial assignment 'init1', and blobs
        b1[0:-1] should be incompatible with b1[-1]. f(b, len(b), []) gives
        the best assignment for blobs 'b'.

        For find_best(b, init), since b[0:-1] are not compatible with b[-1], we
        could reduce it to a smaller problem to find best assignment for b[0:-1]
        as
            find_best(b, init) = min {
                f(b[0:-1], len(b) - 1, init - x) + [x, b[-1]] for x in init, or
                f(b[0:-1], len(b) - 1, init) + [b[-1]]
            }
        where min{} gives the assignment with minimum memory usage.
    '''

    def _get_compatible_prev(candidate_range, best_assignments, cur_idx):
        ''' Find closest position k of best_assignments that is independent of
            candidate_range that candiate_range is compatible with all assignments
            in best_assignments[k].
            Return -1 if not found.
        '''
        def is_compatible_all(candidate_range, assignments):
            ''' return true if compatible for all assignments in assignments '''
            return all([is_compatible(candidate_range[1], x, []) for x in assignments])

        ii = cur_idx - 1
        while ii >= 0:
            cba = best_assignments[ii]
            if is_compatible_all(candidate_range, cba):
                return ii
            ii -= 1
        return -1

    def _find_best(ranges, init_assignment, prev_best_assignment, counter):
        ''' Find the best assignment for blobs 'ranges' given an initialized
            assignment 'init_assignment'.

            Blobs in ranges[0:-1] should be incompatible with blob range[-1].
            'prev_best_assignment': best assignment for blobs in ranges[:-1]

            By assigning ranges[-1] to each assignment k in 'init_assignment' or
            in a new assignment, the problem becomes a smaller problem to find
            the best assignment for ranges[0:-1] given the initial assignment
            init_assigment[0:k, (k+1):-1].
        '''
        # Blob to check
        find_range = ranges[-1]
        # Blobs in ranges[0:-1] are incompatible with ranges[-1] so that we can
        # reduce it to a smaller problem.
        assert all(not is_compatible(x[1], [find_range], []) for x in ranges[0:-1])

        sz = len(init_assignment)
        best_candidates = []
        # Try to assign 'find_range' to each assignment in init_assignment
        for ii in range(sz):
            if not is_compatible(find_range[1], init_assignment[ii], []):
                continue
            cur_best = copy.deepcopy(init_assignment)
            cur_best[ii].append(find_range)
            if len(ranges) > 1:
                cur_best_tmp = [x for i, x in enumerate(cur_best) if i != ii]
                # reduce to a smaller dp problem
                cur_best_tmp = compute_assignments_dp(
                    ranges[:-1], cur_best_tmp, counter)
                cur_best = cur_best_tmp + [cur_best[ii]]
            best_candidates.append(cur_best)
        # Try to put 'find_range' in a new assignment
        best_candidates.append(prev_best_assignment + [[find_range]])

        ret = min(best_candidates, key=lambda x: get_memory_usage(x))
        return ret

    if not counter:
        counter = [0]
    counter[0] += 1

    if counter and counter[0] % 5000 == 0:
        rs = [ranges_sorted[0][1].defined, ranges_sorted[-1][1].used]
        log.info('Finding assignments {} ({} -> {})...'.format(
            counter[0], rs[0], rs[1]))

    init_assignment = init_assignment or []
    # best_assignments[k]: best assignments for first k blobs ranges_sorted[0:(k+1)]
    best_assignments = []
    # Find best assignment for blobs ranges_sorted[0:ii]
    for ii, cur_range in enumerate(ranges_sorted):
        # closest best_assignment that is independent of ranges_sorted[ii]
        prev_idx = _get_compatible_prev(cur_range, best_assignments, ii)
        prev_best = copy.deepcopy(init_assignment) if prev_idx < 0 else \
                    copy.deepcopy(best_assignments[prev_idx])
        # Need to find best assignment for blobs in 'ranges_part'
        ranges_part = ranges_sorted[(prev_idx + 1):(ii + 1)]
        cur_best = _find_best(
            ranges_part, prev_best,
            best_assignments[-1] if best_assignments else init_assignment,
            counter)
        assert _get_count(cur_best) == _get_count(prev_best) + len(ranges_part)
        best_assignments.append(copy.deepcopy(cur_best))

    assert len(best_assignments) == len(ranges_sorted)

    best = best_assignments[-1]

    return best
