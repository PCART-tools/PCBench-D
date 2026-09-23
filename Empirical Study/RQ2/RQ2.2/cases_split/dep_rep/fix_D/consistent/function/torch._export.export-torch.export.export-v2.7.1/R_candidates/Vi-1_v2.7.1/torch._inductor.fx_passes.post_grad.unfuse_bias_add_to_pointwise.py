@register_graph_pattern(
    CallFunction(aten.addmm, KeywordArg("inp"), Arg(), Arg()),
    pass_dict=pass_patterns[2],
    extra_check=should_prefer_unfused_addmm,
)
def unfuse_bias_add_to_pointwise(match: Match, mat1, mat2, *, inp):
    def repl(inp, x1, x2):
        return x1 @ x2 + inp

    match.replace_by_example(repl, [inp, mat1, mat2])
