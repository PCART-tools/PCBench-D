    def _register_weight_pack_pass():
        @register_freezing_graph_pattern(
            CallFunction(aten.convolution.default, *_aten_conv_args),
            extra_check=_is_packable_convolution,
        )
        def convolution(match, *args, **kwargs):
            is_transposed = kwargs.get("is_transposed")
            assert isinstance(is_transposed, bool)
            graph = match.graph
            conv_node = match.output_node()
            input_size = conv_node.args[0].meta.get("val").shape
            with graph.inserting_before(conv_node):
                constant_args = [args[4], args[3], args[5], args[-1]]
                packed_weight_op = mkldnn._reorder_convolution_weight
                packed_conv_op = mkldnn._convolution_pointwise.default
                if is_transposed:
                    constant_args.insert(1, args[-2])  # output_padding
                    packed_weight_op = mkldnn._reorder_convolution_transpose_weight
                    packed_conv_op = mkldnn._convolution_transpose_pointwise.default
                if not has_free_symbols(input_size):
                    packed_weight_inputs = (
                        (args[1],) + tuple(constant_args) + (input_size,)
                    )
                    packed_weight_node = graph.create_node(
                        "call_function", packed_weight_op, args=packed_weight_inputs
                    )
                else:
                    assert not is_transposed
                    # For dynamic shape case, we need to pack weight in runtime.
                    packed_weight_node = args[1]
                packed_conv_inputs = (
                    (args[0], packed_weight_node, args[2])
                    + tuple(constant_args)
                    + ("none", [], "")
                )
                packed_conv_node = graph.create_node(
                    "call_function", packed_conv_op, tuple(packed_conv_inputs)
                )
                conv_node.replace_all_uses_with(packed_conv_node)
                packed_conv_node.meta.update(conv_node.meta)
                graph.erase_node(conv_node)
            counters["inductor"]["mkldnn_conv_weight_pack_matcher_count"] += 1
            counters["inductor"]["mkldnn_conv_weight_pack_matcher_nodes"] += len(
                match.nodes
            )

        @register_freezing_graph_pattern(
            CallFunction(aten.mkldnn_rnn_layer.default, *_aten_mkldnn_rnn_layer_args),
            extra_check=_is_packable_mkldnn_rnn_layer,
        )
        def mkldnn_rnn_layer(match, *args, **kwargs):
            def get_item(graph, node, index):
                return graph.call_function(operator.getitem, (node, index))

            graph = match.graph
            lstm_node = match.output_node()
            weight0, weight1 = args[1:3]
            reverse = kwargs.get("reverse")
            packed_lstm_op = aten.mkldnn_rnn_layer.default
            hidden_size = args[9]
            has_biases = args[11]
            batch_first = args[13]
            with graph.inserting_before(lstm_node):
                packed_weight_op = mkldnn._reorder_mkldnn_rnn_layer_weight.default
                packed_weight_inputs = (
                    weight0,
                    weight1,
                    hidden_size,
                    reverse,
                    has_biases,
                    batch_first,
                )
                packed_weight_node = graph.create_node(
                    "call_function", packed_weight_op, packed_weight_inputs, {}, "name"
                )
                packed_weight_items = [
                    get_item(graph, packed_weight_node, i) for i in range(2)
                ]
                pack_lstm_inputs = (
                    args[0],
                    *packed_weight_items,
                    args[3],
                    args[4],
                    args[5],
                    args[6],
                    reverse,
                    *args[7:],
                )

                packed_lstm_node = graph.create_node(
                    "call_function", packed_lstm_op, args=pack_lstm_inputs
                )
                lstm_node.replace_all_uses_with(packed_lstm_node)
                packed_lstm_node.meta.update(lstm_node.meta)
                graph.erase_node(lstm_node)
            counters["inductor"]["mkldnn_rnn_weight_pack_matcher_count"] += 1
            counters["inductor"]["mkldnn_rnn_weight_pack_matcher_nodes"] += len(
                match.nodes
            )

        @register_freezing_graph_pattern(
            CallFunction(
                aten.addmm.default,
                Arg(),
                Arg(),
                Arg(),
                beta=KeywordArg("beta"),
                alpha=KeywordArg("alpha"),
            ),
            extra_check=_is_packable_linear,
            pass_number=1,
        )
        @register_freezing_graph_pattern(
            CallFunction(aten.mm.default, Arg(), Arg()),
            extra_check=_is_packable_linear,
            pass_number=1,
        )
        def linear(match, *args, **kwargs):
            graph = match.graph
            linear_node = match.output_node()
            input = args[0] if linear_node.target == aten.mm.default else args[1]
            bias = (
                None
                if linear_node.target == aten.mm.default
                or (
                    linear_node.target == aten.addmm.default
                    and linear_node.kwargs.get("beta", 1.0) == 0.0
                )
                else args[0]
            )
            weight = args[1] if linear_node.target == aten.mm.default else args[2]
            with graph.inserting_before(linear_node):
                transpose_weight_node = graph.create_node(
                    "call_function", aten.permute.default, (weight, (1, 0))
                )
                weight_dtype = weight.meta.get("val").dtype
                is_lp_weight = weight_dtype in (
                    torch.bfloat16,
                    torch.float16,
                )
                batch_size = input.meta.get("val").shape[0]
                if has_free_symbols(batch_size):
                    assert is_lp_weight or mkldnn._is_mkldnn_acl_supported(), (
                        f"only bf16/fp16 weight prepacking supports dynamic shape inputs but got {weight_dtype}"
                    )
                # For bfloat16 dynamic shape path, using input size hint to pack weight for a better performance.
                packed_weight_inputs = (
                    transpose_weight_node,
                    batch_size.node.shape_env.size_hint(batch_size.node.expr)
                    if has_free_symbols(batch_size)
                    else batch_size,
                )
                # MKL packed matrix can't be copied to a different address because the internal implementation
                # depends on the alignment of internally-stored metadata.
                # In aot mode, we need to firstly save the packed weight, when loading it,
                # it will be in a different address which doesn't work.
                # Disable MKL prepack linear in AOT mode
                packed_weight_op = (
                    mkldnn._reorder_linear_weight
                    if (
                        is_lp_weight
                        or mkldnn._is_mkldnn_acl_supported()
                        or V.aot_compilation
                    )
                    else torch.ops.mkl._mkl_reorder_linear_weight
                )
                packed_weight_node = graph.create_node(
                    "call_function", packed_weight_op, args=packed_weight_inputs
                )

                packed_linear_inputs: tuple[Any, ...] = (input, packed_weight_node)
                if (
                    is_lp_weight
                    or mkldnn._is_mkldnn_acl_supported()
                    or V.aot_compilation
                ):
                    packed_linear_inputs += (bias, "none", [], "")
                    packed_linear_op = mkldnn._linear_pointwise.default
                else:
                    packed_linear_inputs += (transpose_weight_node, bias, batch_size)
                    packed_linear_op = torch.ops.mkl._mkl_linear
                packed_linear_node = graph.create_node(
                    "call_function", packed_linear_op, packed_linear_inputs
                )
                linear_node.replace_all_uses_with(packed_linear_node)
                packed_linear_node.meta.update(linear_node.meta)
                graph.erase_node(linear_node)
            counters["inductor"]["mkldnn_linear_weight_pack_matcher_count"] += 1
            counters["inductor"]["mkldnn_linear_weight_pack_matcher_nodes"] += len(
                match.nodes
            )
