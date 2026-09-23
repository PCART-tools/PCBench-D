def add_if_op(if_net, cond_blob, lexical_scope, then_net, else_net=None):
    """
    A helper function to add an If op to the net.
    Automatically determines whether blobs in the then/else subnets are external
    (from the outer workspace) or local (visible only inside subnet's workspace)
    based on lexical scope - set of all outer blob names visible to the 'If'
    operator. All the blobs in then/else subnets with names matching a name in lexical
    scope and all the blobs that are first used as the operators' inputs are
    considered outer blobs - these blobs must exist in the outer workspace,
    then/else subnets can read their values and new values written into these blobs
    will be visible outside of the 'If' operator. All other blobs are local - exist
    only within inner workspaces for then/else.
    Inputs:
        if_net - net to add an If op to;
        cond_blob - scalar bool blob reference, used as If condition;
        lexical_scope - a set of outer blob names visible to then/else branches;
        then_net/else_net - nets (core.Net) for then/else branches
    """
    then_input_blob_names, then_output_blob_names = get_external_blob_names(
        then_net, lexical_scope)

    else_input_blob_names = set()
    else_output_blob_names = set()
    if else_net:
        else_input_blob_names, else_output_blob_names = get_external_blob_names(
            else_net, lexical_scope)

    input_blob_names = then_input_blob_names | else_input_blob_names
    output_blob_names = then_output_blob_names | else_output_blob_names

    if_inputs = [cond_blob]
    if_inputs += [core.BlobReference(name=b, net=None) for b in input_blob_names]
    if_outputs = [core.BlobReference(name=b, net=None) for b in output_blob_names]

    do_then_net = core.Net('do_then_net')

    then_input_blobs = \
        [core.BlobReference(name=b, net=None) for b in then_input_blob_names]
    then_output_blobs = \
        [core.BlobReference(name=b, net=None) for b in then_output_blob_names]
    then_input_output_names_ordered = [
        str(b) for b in (then_input_blobs + then_output_blobs)]

    then_outer_blob_names = list(then_input_blob_names | then_output_blob_names)
    then_outer_blob_names_idx = [
        then_input_output_names_ordered.index(b) for b in then_outer_blob_names]

    # make sure to use net's name to have unique blob name across multiple subnets
    do_then_workspace_blob = if_net.NextScopedBlob(if_net.Name() + '/workspace_if_then')
    then_input_blobs.append(do_then_workspace_blob)
    then_output_blobs.append(do_then_workspace_blob)
    # make sure that added workspace pointer blobs are in if inputs/outputs
    if_inputs.append(do_then_workspace_blob)
    if_outputs.append(do_then_workspace_blob)

    do_then_net.Do(
        then_input_blobs,
        then_output_blobs,
        net=then_net.Proto(),
        inner_blobs=then_outer_blob_names,
        outer_blobs_idx=then_outer_blob_names_idx)
    do_then_net.AddExternalOutput(*then_output_blobs)

    if_args = {}
    if_args['then_net'] = do_then_net.Proto()

    do_else_workspace_blob = None
    if else_net:
        do_else_net = core.Net('do_else_net')

        else_input_blobs = \
            [core.BlobReference(name=b, net=None) for b in else_input_blob_names]
        else_output_blobs = \
            [core.BlobReference(name=b, net=None) for b in else_output_blob_names]
        else_input_output_names_ordered = [
            str(b) for b in (else_input_blobs + else_output_blobs)]

        else_outer_blob_names = list(else_input_blob_names | else_output_blob_names)
        else_outer_blob_names_idx = [
            else_input_output_names_ordered.index(b) for b in else_outer_blob_names]

        do_else_workspace_blob = \
            if_net.NextScopedBlob(if_net.Name() + '/workspace_if_else')
        else_input_blobs.append(do_else_workspace_blob)
        else_output_blobs.append(do_else_workspace_blob)
        # make sure that added workspace pointer blobs are in if inputs/outputs
        if_inputs.append(do_else_workspace_blob)
        if_outputs.append(do_else_workspace_blob)

        do_else_net.Do(
            else_input_blobs,
            else_output_blobs,
            net=else_net.Proto(),
            inner_blobs=else_outer_blob_names,
            outer_blobs_idx=else_outer_blob_names_idx)
        do_else_net.AddExternalOutput(*else_output_blobs)
        if_args['else_net'] = do_else_net.Proto()

    if_net.CreateScope([], [do_then_workspace_blob])
    if do_else_workspace_blob:
        if_net.CreateScope([], [do_else_workspace_blob])
    if_net.If(if_inputs, if_outputs, **if_args)
    if_net.AddExternalOutput(*if_outputs)
