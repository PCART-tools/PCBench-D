def add_while_op(
        while_net, cond_blob, lexical_scope, loop_body_net, condition_body_net=None):
    """
    A helper function to add a While op to the net. Same rules for determining
    outer and inner blobs as for the 'If' operator apply for the 'While' operator
    loop and condition subnets. If specified, condition net is executed in a separate
    workspace before the first and after each iteration, the last operator must have
    a single scalar boolean output that is written into the condition blob.
    Inputs:
        while_net - net to add a While op to;
        cond_blob - scalar bool blob reference, used as a stop condition;
        lexical_scope - a set of outer blob names visible to the loop's body;
        loop_body_net - net to execute on each iteration;
        condition_body_net - net to compute condition value
    """
    input_blob_names, output_blob_names = get_external_blob_names(
        loop_body_net, lexical_scope)

    # Since it's possible that loop is not going to run even once
    # we have to add loop's external outputs into inputs
    input_blob_names |= output_blob_names

    loop_inputs = [core.BlobReference(name=b, net=None) for b in input_blob_names]
    loop_outputs = [core.BlobReference(name=b, net=None) for b in output_blob_names]

    while_inputs = [cond_blob] + loop_inputs
    while_outputs = [] + loop_outputs

    do_loop_body_net = core.Net('do_loop_body_net')

    loop_input_output_names_ordered = [
        str(b) for b in (loop_inputs + loop_outputs)]
    loop_body_outer_blob_names = list(input_blob_names | output_blob_names)
    loop_body_outer_blob_names_idx = [
        loop_input_output_names_ordered.index(b) for b in loop_body_outer_blob_names]

    do_loop_body_workspace_blob = \
        while_net.NextScopedBlob(while_net.Name() + '/workspace_loop_body')

    loop_inputs.append(do_loop_body_workspace_blob)
    loop_outputs.append(do_loop_body_workspace_blob)
    # make sure that added workspace pointer blobs are in While inputs/outputs
    while_inputs.append(do_loop_body_workspace_blob)
    while_outputs.append(do_loop_body_workspace_blob)

    do_loop_body_net.Do(
        loop_inputs,
        loop_outputs,
        net=loop_body_net.Proto(),
        inner_blobs=loop_body_outer_blob_names,
        outer_blobs_idx=loop_body_outer_blob_names_idx,
        copy_external_blobs=True)
    do_loop_body_net.AddExternalOutput(*loop_outputs)

    while_args = {}
    while_args['loop_net'] = do_loop_body_net.Proto()

    cond_workspace_blob = None
    if condition_body_net:
        cond_input_blob_names, cond_output_blob_names = get_external_blob_names(
            condition_body_net, lexical_scope)

        # make sure condition blob is written by condition net and is
        # visible outside of it
        found_condition_output = False
        for op in condition_body_net.Proto().op:
            if str(cond_blob) in op.output:
                found_condition_output = True
                break
        assert found_condition_output, \
            "Condition net does not write into condition blob"
        if str(cond_blob) not in cond_output_blob_names:
            cond_output_blob_names.add(str(cond_blob))

        cond_inputs = [core.BlobReference(name=b, net=None)
                        for b in cond_input_blob_names]
        assert str(cond_blob) in cond_output_blob_names, \
            'Condition blob expected in condition net output'
        cond_outputs = [core.BlobReference(name=b, net=None)
                        for b in cond_output_blob_names]

        condition_net = core.Net('do_loop_condition_net')

        cond_input_output_names_ordered = [
            str(b) for b in (cond_inputs + cond_outputs)]
        cond_body_outer_blob_names = \
            list(cond_input_blob_names | cond_output_blob_names)
        cond_body_outer_blob_names_idx = [
            cond_input_output_names_ordered.index(b)
            for b in cond_body_outer_blob_names]

        cond_workspace_blob = \
            while_net.NextScopedBlob(while_net.Name() + '/workspace_loop_cond')
        cond_inputs.append(cond_workspace_blob)
        cond_outputs.append(cond_workspace_blob)

        condition_net.Do(
            cond_inputs,
            cond_outputs,
            net=condition_body_net.Proto(),
            inner_blobs=cond_body_outer_blob_names,
            outer_blobs_idx=cond_body_outer_blob_names_idx)
        condition_net.AddExternalOutput(*cond_outputs)

        while_args['cond_net'] = condition_net.Proto()

        while_inputs += [b for b in cond_inputs
                            if str(b) not in input_blob_names]
        while_outputs += [b for b in cond_outputs
                            if str(b) not in output_blob_names]

        if str(cond_blob) not in lexical_scope:
            while_net.ConstantFill(
                [],
                cond_blob,
                dtype=core.DataType.BOOL,
                value=False)

    while_net.CreateScope([], [do_loop_body_workspace_blob])
    if cond_workspace_blob:
        while_net.CreateScope([], [cond_workspace_blob])
    while_net.While(while_inputs, while_outputs, **while_args)
    while_net.AddExternalOutput(*while_outputs)
