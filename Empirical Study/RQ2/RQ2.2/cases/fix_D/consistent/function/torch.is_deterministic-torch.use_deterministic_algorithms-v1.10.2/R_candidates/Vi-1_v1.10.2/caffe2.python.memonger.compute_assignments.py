def compute_assignments(ranges, static_blobs, algo):
    '''
    algo: Method used to find assignments (AssignmentAlgorithm.GREEDY or
          AssignmentAlgorithm.DYNAMIC_PROGRAMMING).
          AssignmentAlgorithm.DYNAMIC_PROGRAMMING gives optimal solution at the
          cost of more computation.
          AssignmentAlgorithm.GREEDY may be better in the case 'blob_sizes' is
          not provided.
    '''

    # Sort the ranges based on when they are last used.
    # If LiveRange.used is None, then the blob is never used and could
    # be consumed externally. Sort these to the end of the list as opposed
    # to the beginning so that they can be shared as well.
    ranges = sorted(
        viewitems(ranges),
        key=lambda p: (p[1].used is None, p[1].used),
    )
    # Update None values
    ranges = get_updated_ranges(ranges)

    # Sharable blobs
    ranges_sharable = [x for x in ranges if x[0] not in static_blobs]
    # Static blobs, not sharable
    ranges_static = [x for x in ranges if x[0] in static_blobs]

    log.info("Total sharable blobs {}".format(len(ranges_sharable)))

    best_assignment = []
    if algo == AssignmentAlgorithm.DYNAMIC_PROGRAMMING:
        best_assignment = compute_assignments_dp(ranges_sharable, [])
    elif algo == AssignmentAlgorithm.GREEDY:
        best_assignment = compute_assignments_greedy(ranges_sharable, [])
    else:
        assert "Invalid algo name {}".format(algo)
    best_assignment += [[x] for x in ranges_static]

    # verify_assignments(best_assignment)

    return best_assignment
