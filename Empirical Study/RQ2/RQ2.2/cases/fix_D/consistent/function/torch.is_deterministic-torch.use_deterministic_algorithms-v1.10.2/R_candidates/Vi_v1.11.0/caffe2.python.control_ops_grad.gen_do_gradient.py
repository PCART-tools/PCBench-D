def gen_do_gradient(op, g_output):
    """
    Generates gradient Do operator, given forward Do op and a list
    of gradient blobs corresponding to forward op's outputs
    Returns a gradient op and a list of blobs corresponding to input gradients
    """
    from caffe2.python.core import BlobReference
    subnet, outer_to_inner_map, inner_to_outer_map, workspace_blob_name = \
        _do_op_sanity_check_and_process(op)

    assert len(g_output) == len(op.output), \
        "Different number of gradient blobs and Do op outputs"

    grad_ops, deduped_g_output = dedupe_g_output(op, g_output)
    g_output = deduped_g_output

    # From the outer net point of view:
    #  Do is an operator that has some number of inputs and outputs;
    #  we have to generate a gradient operator that writes into
    #  corresponding input gradient blobs and has access to inputs, outputs
    #  and gradient output blobs
    # From the inner net point of view:
    #  Do is an operator with a subnet and blob bindings,
    #  we need to forward Do's output blob gradients into inner workspace,
    #  use them to run backward pass generation and forward Do's input blob
    #  gradients back into outer workspace

    op_output = [str(o) for o in op.output]
    op_output = op_output[:-1]  # remove workspace pointer blob
    op_input = [str(i) for i in op.input]
    op_input = op_input[:-1]  # remove workspace pointer blob

    ordered_inner_output_blob_names = [outer_to_inner_map[o] for o in op_output]

    backward_pass_initial_grad_map = {}
    initial_grad_map = {}
    for inner_output_name, outer_grad_output_name in \
            zip(ordered_inner_output_blob_names, g_output):
        # link inner_output_name to corresponding inner_grad_output_name for
        # backward pass generation;
        if outer_grad_output_name:
            inner_grad_output_name = inner_output_name + "/_DO_OPERATOR_INNER_GRAD_"
            backward_pass_initial_grad_map[BlobReference(inner_output_name)] = \
                BlobReference(inner_grad_output_name)
            initial_grad_map[inner_grad_output_name] = str(outer_grad_output_name)
    assert len(initial_grad_map) > 0, "Empty initial gradient map for Do op"

    inner_grad_ops, inner_grad_names_map = _gen_subgradient_pass(
        subnet, backward_pass_initial_grad_map)

    if len(inner_grad_ops) == 0:
        return [], []

    grad_copy_ops = []
    g_input = []
    new_op_outputs = []
    new_blob_bindings = {}
    for outer_input_name in op_input:
        inner_input_name = outer_to_inner_map[outer_input_name]
        if inner_input_name in inner_grad_names_map:
            inner_grad_input_name = inner_grad_names_map[inner_input_name]
            outer_grad_input_name = outer_input_name + "_grad"

            # It is possible that inner_grad_input_name will need to be
            # linked to another outer blob. For example:
            #
            #    // y - param initialized in init_net
            #    x = ...
            #    z = ...
            #    with ops.IfNet(...):
            #        ops.Add([z, x], y) # inner Do block
            #    loss = f(..., y, ...)
            #
            # In this case x, y and z are external for the inner Do block,
            # the inputs of the Do block are z and x and the output is y.
            # When computing the gradient of input x given the gradient
            # of output y it's easy to see that they are equal.
            # During the generation of gradient Do operator, we link
            # external gradient y (y_grad) to the internal name
            # (y/_DO_OPERATOR_INNER_GRAD_) and generate the backward pass
            # for the internal Do net. As a result we get gradient operators
            # for the gradient Do and gradient map that maps internal Do
            # blobs to their computed gradients.
            # In this example, gradient map may have blob x linked to
            # gradient blob y/_DO_OPERATOR_INNER_GRAD_.
            # We should export gradient for x outside of Do, so
            # we add a blob mapping from inner gradient blob
            # (y/_DO_OPERATOR_INNER_GRAD_) to a new outer name (x_grad).
            #
            # (Note: since we use transparent blob mapping between outer and
            # inner (Do's) workspace, these operations do not involve copying
            # but are merely using blobs in outer workspace in the Do's operator
            # workspace under (possibly) different names)
            #
            # At the same time, we need to add a blob mapping from inner name
            # y/_DO_OPERATOR_INNER_GRAD_ to the outer blob y_grad
            # Hence in this case, we cannot use existing blob mapping scheme
            # that requires a bijection between subset of inner blob names and
            # a set of all (Do's input and output) outer blob names

            # TODO(iliacher): Remove unnecessary blob copying

            new_inner_grad_input_name = \
                inner_input_name + "/_DO_OPERATOR_INNER_GRAD_COPY_"
            grad_copy_ops.append(_prepare_blob_copy_op(
                inner_grad_input_name, new_inner_grad_input_name))

            new_blob_bindings[new_inner_grad_input_name] = outer_grad_input_name
            new_op_outputs.append(outer_grad_input_name)
            g_input.append(outer_grad_input_name)
        else:
            g_input.append(None)

    new_op_inputs = []
    overwritten_names = set()
    saved_local_blob_names = set()
    for grad_op in inner_grad_ops:
        grad_op_input = [str(i) for i in grad_op.input]
        grad_op_output = [str(o) for o in grad_op.output]
        for grad_op_input_name in grad_op_input:
            if grad_op_input_name in overwritten_names:
                continue
            # check if this is an external blob
            outer_name = inner_to_outer_map.get(grad_op_input_name, None)
            if not outer_name:
                # check if this is an external gradient blob
                outer_name = initial_grad_map.get(grad_op_input_name, None)
            if outer_name:
                outer_name = str(outer_name)
                if outer_name not in new_op_inputs:
                    new_op_inputs.append(outer_name)

                new_blob_bindings[grad_op_input_name] = outer_name
            else:
                # this is a local blob, we'll get it's value from
                # a saved forward op workspace
                saved_local_blob_names.add(grad_op_input_name)
        overwritten_names.update(grad_op_output)

    # add inner gradient copy ops
    inner_grad_ops += grad_copy_ops

    gradient_do_def = _prepare_gradient_do_op(
        fwd_op=op,
        fwd_net=subnet,
        grad_ops=inner_grad_ops,
        inputs=new_op_inputs,
        outputs=new_op_outputs,
        blob_bindings=new_blob_bindings,
        saved_fwd_blobs=saved_local_blob_names,
        workspace_blob_name=workspace_blob_name)
    grad_ops.append(gradient_do_def)

    _do_op_sanity_check_and_process(gradient_do_def)

    return grad_ops, g_input
