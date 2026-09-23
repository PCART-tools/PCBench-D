def compute_assignments_greedy(ranges_sorted, init_assignments=None):
    assignments = init_assignments or []
    visited = {y[0] for x in assignments for y in x}

    for (name, range_) in ranges_sorted:
        if name in visited:
            continue
        assigned = False
        best_assignment = 0
        min_dist = float("inf")
        candidate_size = range_.size or 0
        for idx, assignment in enumerate(assignments):
            if is_compatible(range_, assignment, []):
                assigned = True
                dist = abs(_get_max_size(assignment) - candidate_size)
                if dist < min_dist:
                    min_dist = dist
                    best_assignment = idx
        if assigned:
            assignment = assignments[best_assignment]
            assignment.append((name, range_))
        else:
            assignments.append([(name, range_)])
    return assignments
