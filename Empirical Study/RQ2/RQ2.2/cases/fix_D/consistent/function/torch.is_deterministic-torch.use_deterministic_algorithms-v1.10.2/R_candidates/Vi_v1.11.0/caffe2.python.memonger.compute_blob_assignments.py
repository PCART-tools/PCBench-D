def compute_blob_assignments(assignments):
    blob_assignments = {}
    for assignment in assignments:
        if len(assignment) == 1:
            continue
        last_blob, _ = assignment[-1]
        for (blob, _) in assignment:
            blob_assignments[blob] = last_blob
    return blob_assignments
