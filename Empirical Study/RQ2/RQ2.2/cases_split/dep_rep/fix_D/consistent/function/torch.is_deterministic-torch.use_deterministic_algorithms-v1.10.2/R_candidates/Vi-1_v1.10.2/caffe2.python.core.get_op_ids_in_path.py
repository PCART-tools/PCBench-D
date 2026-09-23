def get_op_ids_in_path(ssa, blob_versions, inputs, outputs):
    """
    Given a ssa and blob_versions as produced by get_ssa(), returns the list
    of op indices that are necessary in order to generate the blobs in
    `outputs`, given blobs in `inputs`.
    Consider that the `inputs` are given in their latest version.
    """
    inputs_set = set((str(i), blob_versions[str(i)]) for i in inputs)
    producers = get_output_producers(ssa)
    queue = [(str(o), blob_versions[str(o)]) for o in outputs]
    used_op_ids = set()
    while len(queue) > 0:
        o = queue.pop()
        if (o not in inputs_set) and (o in producers):
            op_id = producers[o]
            if op_id not in used_op_ids:
                used_op_ids |= {op_id}
                inputs, _ = ssa[op_id]
                queue.extend(inputs)
    return sorted(used_op_ids)
