    @substitute_in_graph(
        optree._C.is_dict_insertion_ordered,
        can_constant_fold_through=True,
    )
    def _(*args: Any, **kwargs: Any) -> bool:
        # In namespace 'torch', the dictionary is always traversed in insertion order.
        # This function returns True.
        raise ValueError(
            "Should not be called directly "
            "because the original function will be called in the constant fold path."
        )
