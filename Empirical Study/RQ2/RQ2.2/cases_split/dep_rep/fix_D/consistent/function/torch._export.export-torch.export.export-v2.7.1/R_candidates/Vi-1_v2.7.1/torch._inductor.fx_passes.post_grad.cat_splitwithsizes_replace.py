@register_lowering_pattern(
    CallFunction(
        aten.split_with_sizes,
        CallFunction(
            aten.cat,
            KeywordArg("input_"),
            Ignored(),
            _users=MULTIPLE,
        ),
        Ignored(),
        Ignored(),
    ),
    pass_number=2,
    extra_check=is_valid_cat_splitwithsizes,
)
def cat_splitwithsizes_replace(match, input_):
    return input_
