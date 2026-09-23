def compute_statistics(assignments):
    blob_bytes = {
        blob: blob_nbytes(blob) for assignment in assignments
        for (blob, _) in assignment}
    baseline_nbytes = sum(viewvalues(blob_bytes))
    optimized_nbytes = sum(
        max(blob_bytes[blob] for (blob, _) in assignment)
        for assignment in assignments)
    return Statistics(
        baseline_nbytes=baseline_nbytes,
        optimized_nbytes=optimized_nbytes)
