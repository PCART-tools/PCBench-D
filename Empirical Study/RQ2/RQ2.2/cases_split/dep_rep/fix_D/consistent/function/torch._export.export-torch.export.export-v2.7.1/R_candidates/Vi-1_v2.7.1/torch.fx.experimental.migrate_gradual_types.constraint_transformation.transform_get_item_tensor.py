@register_transformation_rule(GetItemTensor)
def transform_get_item_tensor(constraint, counter):
    """
    When the index is a tuple, then the output will be a tensor
    TODO: we have to check if this is the case for all HF models

    The cases we are covering here are a tuple with one of:
     - slice with default argument
     - None

     None appends 1 to the input tensor dimensions
     so each occurrence of 'None' increases the rank by 1

     slice with default arguments does not change the rank
    """
    assert isinstance(constraint.index_tuple, tuple)

    # generate a result tensor of the expected size
    dims, counter = gen_tensor_dims(constraint.tensor_size, counter)
    nat_constraints = gen_nat_constraints(dims)

    # generate a place-holder list of the right rank
    # where "slice" does not contribute to the rank and "None" does
    none_c = constraint.index_tuple.count(None)
    resulting_tensor_dims = (none_c + len(dims)) * [None]

    dim_index = 0
    for i in range(len(constraint.index_tuple)):
        # append 1 to the right location of the resulting tensor
        if constraint.index_tuple[i] is None:
            resulting_tensor_dims[i] = 1

        elif constraint.index_tuple[i] == slice(None, None, None):
            pass

        else:
            raise NotImplementedError("Method not yet implemented")

    # append the remaining dimensions to the right location
    dim_index = 0
    for i in range(len(resulting_tensor_dims)):
        if resulting_tensor_dims[i] is None:
            resulting_tensor_dims[i] = dims[dim_index]
            dim_index += 1

    # check if the index is valid
    is_valid_index = valid_index_tensor(constraint.index_tuple, dims)

    # check if the resulting tensor is within bounds
    if len(resulting_tensor_dims) > 4:
        return F(), counter

    else:
        constraints = [
            BinConstraintT(constraint.input_var, TensorType(dims), op_eq),
            BinConstraintT(constraint.res, TensorType(resulting_tensor_dims), op_eq),
            *nat_constraints,
            is_valid_index,
        ]
        return Conj(constraints), counter
