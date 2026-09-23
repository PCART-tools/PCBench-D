def rewrite_for_scripting(mod: torch.nn.Module) -> torch.nn.Module:
    """
    Makes the dynamically dispatched ops in `mod` be explicit, so they
    can be visibile to `torch.jit.script`. In detail:

    1. symbolically traces the forward with FX, without any leaves
    2. for each quantizeable op with dynamic dispatch, rewrites the graph to
       contain the quantized subgraph (quant if necessary, quantized op,
       dequant if necessary).
    3. recursively repeat (1 - 2) for each child
    """

    def rewrite_helper(mod : torch.nn.Module):
        copied = copy.copy(mod)
        for name, child in mod.named_children():
            setattr(copied, name, rewrite_helper(child))

        if hasattr(mod, '_auto_quant_state') and (
            mod._auto_quant_state.has_at_least_one_seen_op_info() or  # type: ignore[union-attr, operator]
            (mod._auto_quant_state.get_output_dtypes() is not None)  # type: ignore[union-attr, operator]
        ):
            copied._auto_quant_state.reset_to_new_call()  # type: ignore[union-attr, operator]

            graph = AllModuleTracer().trace(copied)
            return torch.fx.GraphModule(copied, graph, copied.__class__.__name__)
        else:
            return copied

    return rewrite_helper(mod)
