def register_acc_op_mapping(
    op_and_target: Tuple[str, Union[str, Callable]],
    arg_replacement_tuples: Optional[
        List[Union[Tuple[Union[str, Tuple[str, ...]], str], Tuple[Union[str, Tuple[str, ...]], str, bool]]]
    ] = None,
    kwargs_to_move_to_acc_out_ty: Optional[List[Tuple[str, str]]] = None,
):
    """
    Use this decorator to map a non-acc operator to an acc operator.

    Args:
        op_and_target: A tuple that contains op and target of the node that represents the non-acc operator.
        arg_replacement_tuples: Please refer to the comment on above for `ArgReplacementTuplesType`.
        kwargs_to_move_to_acc_out_ty: The kwargs we want to move out from the non-acc op kwargs to acc_out_ty.
    """

    def insert(new_fn_target: Callable):
        # If arg_replacement_tuples is None then assume we use the same signature for
        # the acc_op and the original op.
        if arg_replacement_tuples is None:
            final_arg_replacement_tuples = _get_dup_signature_tuples(new_fn_target)
        else:
            final_arg_replacement_tuples = arg_replacement_tuples  # type: ignore[assignment]

        _insert_fun(
            op_and_target=op_and_target,
            new_fn_target=new_fn_target,
            arg_replacement_tuples=final_arg_replacement_tuples,  # type: ignore[arg-type]
            kwargs_to_move_to_acc_out_ty=kwargs_to_move_to_acc_out_ty,
        )
        return new_fn_target

    return insert
