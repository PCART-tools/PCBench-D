def setup_rnn_tests():
    layers_opts = [
        (1, "unilayer"),
        (3, "trilayer")
    ]
    bidirectional_opts = [
        (False, "forward"),
        (True, "bidirectional")
    ]
    initial_state_opts = [
        (True, "with_initial_state"),
        (False, "no_initial_state")
    ]
    variable_length_opts = [
        (0, "without_sequence_lengths"),
        (1, "with_variable_length_sequences"),
        (2, "with_batch_first_sequence_lengths")
    ]
    dropout_opts = [
        (0.2, "with_dropout"),
        (0.0, "without_dropout")
    ]
    test_count = 0
    for (layer, bidirectional, initial_state, variable_length, dropout) in \
            itertools.product(
                layers_opts,
                bidirectional_opts,
                initial_state_opts,
                variable_length_opts,
                dropout_opts,):

        for base, name, extra_kwargs in (
                ("elman", "elman_relu", {"nonlinearity": u"relu"}),
                ("elman", "elman_tanh", {"nonlinearity": u"tanh"}),
                ("lstm", "lstm", {}),
                ("gru", "gru", {})
        ):
            # Need Add between list of tensors
            script_test_min_opset_version = 11

            if (    # compiling in script mode fails with errors like:
                    # torch.jit.frontend.UnsupportedNodeError: annotated assignments
                    # without assigned value aren't supported
                    # https://msdata.visualstudio.com/Vienna/_workitems/edit/1160723
                    base == 'elman' or
                    # compiling in script mode fails with errors like:
                    # RuntimeError: Arguments for call are not valid.
                    # https://msdata.visualstudio.com/Vienna/_workitems/edit/1160723
                    base == 'lstm'):
                script_test_min_opset_version = float("inf")
            make_test(name, base, layer, bidirectional, initial_state,
                      variable_length, dropout, script_test_min_opset_version,
                      **extra_kwargs)
            test_count += 1

    # sanity check that a representative example does exist
    TestONNXRuntime.test_gru_trilayer_forward_with_initial_state_without_sequence_lengths_with_dropout

    # make sure no one accidentally disables all the tests without
    # noticing
    if test_count != 192:
        raise ValueError("Expected 192 tests but found {}".format(test_count))
