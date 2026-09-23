def unlift_tokens(fw_module, fw_metadata, aot_config, bw_module=None):
    # Remove the tokens from the inputs/outputs of the graph since inductor does
    # not want these extra inputs/outputs, and replace them with
    # _make_token() to create a token, and _sink_tokens() to collect the
    # tokens.  See Note [Side-Effectful Tokens in AOTAutograd]
    # Logic:
    # 1. Inputs identified as input tokens:
    #    - If used as a first argument in with_effects
    #
    # 2. Outputs identified as output tokens:
    #    - If Produced by getitem(with_effects, 0)
    #
    # 3. Checks invariants of number input output tokens:
    # forward:
    # expected_num_erased_inputs == len(fw_metadata.tokens)
    # expected_num_erased_outputs == len(fw_metadata.tokens)
    # backward:
    # expected_num_erased_inputs == fw_metadata.num_backward_tokens
    # expected_num_erased_outputs == fw_metadata.num_backward_tokens
    num_forward_tokens = len(fw_metadata.tokens)
    num_backward_tokens = fw_metadata.num_backward_tokens

    def rewrite_with_effects_input_token(module, node):
        with module.graph.inserting_before(node):
            new_token_node = module.graph.call_function(
                torch.ops.prims._make_token.default, ()
            )
            new_token_node.meta["val"] = torch.tensor([])
            new_token_node.meta["tensor_meta"] = torch.tensor([])

            args = list(node.args)
            args[0] = new_token_node
            node.args = tuple(args)

    def rewrite_output(module, node, output_token_nodes, other_output_args):
        for output_token_node in output_token_nodes:
            assert (
                output_token_node.op == "call_function"
                and output_token_node.target == operator.getitem
                and output_token_node.args[1] == 0
            )
        with module.graph.inserting_before(node):
            module.graph.call_function(
                torch.ops.prims._sink_tokens.default,
                (output_token_nodes,),
            )
            node.args = (other_output_args,)

    def do(module, subgraph, expected_num_erased):
        num_erased_inputs = 0
        num_erased_outs = 0
        input_nodes = []
        input_token_nodes = set()
        with_effect_nodes = []
        output_token_nodes = []
        other_output_nodes = []
        for node in module.graph.nodes:
            if node.op == "placeholder":
                input_nodes.append(node)
            elif is_with_effects(node):
                with_effect_nodes.append(node)
                if node.args[0] in input_nodes:
                    input_token_nodes.add(node.args[0])
                    rewrite_with_effects_input_token(module, node)
            elif node.op == "output":
                outs = node.args[0]
                for out in outs:
                    if (
                        isinstance(out, torch.fx.node.Node)
                        and out.op == "call_function"
                        and out.target == operator.getitem
                        and out.args[1] == 0
                        and out.args[0] in with_effect_nodes
                    ):
                        output_token_nodes.append(out)
                    else:
                        other_output_nodes.append(out)

                rewrite_output(module, node, output_token_nodes, other_output_nodes)
                num_erased_outs = len(output_token_nodes)

        for input_token_node in input_token_nodes:
            module.graph.erase_node(input_token_node)

        num_erased_inputs = len(input_token_nodes)

        assert (
            num_erased_inputs == expected_num_erased
        ), f"{subgraph} num_erased_inputs:{num_erased_inputs} {input_token_nodes}!=expected {expected_num_erased}"
        assert (
            num_erased_outs == expected_num_erased
        ), f"{subgraph} num_erased_outs:{num_erased_outs} {output_token_nodes}!=expected {expected_num_erased}"

        module.recompile()

    if num_forward_tokens > 0:
        if aot_config.enable_log:
            from torch._dynamo.utils import lazy_format_graph_code

            aot_graphs_effects_log.debug(
                "%s",
                lazy_format_graph_code(
                    "Forward graph before unlifting tokens",
                    fw_module,
                    aot_config.aot_id,
                    include_stride=True,
                    include_device=True,
                    colored=True,
                ),
            )
        do(
            fw_module,
            "forward",
            num_forward_tokens,
        )

    if bw_module is not None and num_backward_tokens > 0:
        if aot_config.enable_log:
            from torch._dynamo.utils import lazy_format_graph_code

            aot_graphs_effects_log.debug(
                "%s",
                lazy_format_graph_code(
                    "Backward graph before unlifting tokens",
                    bw_module,
                    aot_config.aot_id,
                    include_stride=True,
                    include_device=True,
                    colored=True,
                ),
            )
        do(bw_module, "backward", num_backward_tokens)

    # This is sad, but we need to update the metadata to get rid of
    # the tokens.
    fw_metadata.tokens = {}
    fw_metadata.num_backward_tokens = 0
