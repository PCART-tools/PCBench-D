def _do_op_sanity_check_and_process(op):
    assert op.type == "Do", "Expected Do op"

    subnet = _get_net_argument(op, "net")
    assert subnet, "No net argument found in Do op"

    inner_blobs = None
    outer_blobs_idx = None
    for arg in op.arg:
        if arg.name and arg.name == "inner_blobs":
            assert not inner_blobs, "inner_blobs redefinition"
            assert arg.strings and len(arg.strings) > 0, \
                "Empty inner_blobs argument in Do op"
            inner_blobs = [s.decode('utf-8') for s in arg.strings]
        if arg.name and arg.name == "outer_blobs_idx":
            assert not outer_blobs_idx, "outer_blobs_idx redefinition"
            assert arg.ints and len(arg.ints) > 0, \
                "Empty outer_blobs_idx argument in Do op"
            outer_blobs_idx = arg.ints
        if inner_blobs and outer_blobs_idx:
            break

    assert inner_blobs, "No inner_blobs argument found in Do op"
    assert outer_blobs_idx, "No outer_blobs_idx argument found in Do op"

    assert len(inner_blobs) == len(outer_blobs_idx), \
        "Arguments inner_blobs and outer_blobs_idx of different length in Do op"

    all_inner_blobs = set(inner_blobs)
    assert len(all_inner_blobs) == len(inner_blobs), \
        "Found duplicates in inner_blobs in Do op"

    op_input = [str(i) for i in op.input]
    assert len(op_input) > 0, "Expected at least one input blob"
    # remove last input blob that holds pointer to workspace
    input_workspace_blob_name = op_input[-1]
    op_input = op_input[:-1]

    op_output = [str(o) for o in op.output]
    assert len(op_output) > 0, "Expected at least one output blob"
    # remove last output blob that holds pointer to workspace
    workspace_blob_name = op_output[-1]
    assert input_workspace_blob_name == workspace_blob_name, \
        "Expected same input/output workspace blob"
    op_output = op_output[:-1]

    all_op_input_blob_names = set(op_input)
    assert len(all_op_input_blob_names) == len(op_input), \
        "Found duplicates in Do op inputs"
    all_op_output_blob_names = set(op_output)
    assert len(all_op_output_blob_names) == len(op_output), \
        "Found duplicates in Do op outputs"

    ordered_outer_blob_names = op_input + op_output
    all_outer_blob_names = set(ordered_outer_blob_names)
    used_outer_blob_names = set()
    outer_to_inner_map = {}
    inner_to_outer_map = {}
    for inner_name, outer_blob_idx in zip(inner_blobs, outer_blobs_idx):
        assert outer_blob_idx >= 0 and \
            outer_blob_idx < len(ordered_outer_blob_names), \
            "Outer blob index is out of bounds in Do op"
        outer_name = ordered_outer_blob_names[outer_blob_idx]
        assert outer_name not in used_outer_blob_names, \
            "Reusage of outer blob name " + outer_name + " in Do op"
        used_outer_blob_names.add(outer_name)
        outer_to_inner_map[outer_name] = inner_name
        inner_to_outer_map[inner_name] = outer_name

    assert len(used_outer_blob_names) == len(all_outer_blob_names), \
        "Not all outer blob names are used in blob bindings in Do op"

    return subnet, outer_to_inner_map, inner_to_outer_map, workspace_blob_name
