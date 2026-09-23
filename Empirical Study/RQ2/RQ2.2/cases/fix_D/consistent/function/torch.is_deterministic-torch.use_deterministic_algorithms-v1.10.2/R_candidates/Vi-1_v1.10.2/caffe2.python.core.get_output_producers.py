def get_output_producers(ssa):
    """
    Given a ssa in the format produced by get_ssa(), returns a map from
    versioned blob into the operator index that produces that version of
    the blob. A versioned blob is a tuple (blob_name, version).
    """
    producers = {}
    for i, (_inputs, outputs) in enumerate(ssa):
        for o in outputs:
            producers[o] = i
    return producers
