def same_dtype(match):
    return match.output_node().args[0].meta["val"].dtype == match.kwargs["dtype"]
