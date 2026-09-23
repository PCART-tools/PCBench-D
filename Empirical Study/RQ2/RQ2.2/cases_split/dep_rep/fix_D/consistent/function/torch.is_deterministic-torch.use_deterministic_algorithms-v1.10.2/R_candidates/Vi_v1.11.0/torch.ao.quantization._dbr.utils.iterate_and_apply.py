def iterate_and_apply(
    args: Any,
    flattened_tensor_infos: List[Optional[QTensorInfo]],
    func: Callable,
    flattened_tensor_infos_idx=None
) -> Any:
    """
    Inputs:
      `args`: arguments to a function, may contain nested types, for example:

        ([torch.Tensor, torch.Tensor], int, (int, int))

      `flattened_tensor_infos`: tensor information containers for each tensor
        in `args`, flattened, for example corresponding with above:

        ({...}, {...}, None, None, None)

      `func`: function to apply to each tensor in `args` to create `new_args`

    Returns `new_args`, where each tensor has been transformed by `func`.
    """
    arg_idx = 0
    if flattened_tensor_infos_idx is None:
        flattened_tensor_infos_idx = [0]

    if isinstance(args, tuple):
        new_args = []
        for arg in args:
            new_arg = iterate_and_apply(
                arg, flattened_tensor_infos, func, flattened_tensor_infos_idx)
            new_args.append(new_arg)
        return tuple(new_args)
    elif isinstance(args, list):
        for idx in range(len(args)):
            new_arg = iterate_and_apply(
                args[idx], flattened_tensor_infos, func, flattened_tensor_infos_idx)
            args[idx] = new_arg
        return args
    else:
        # individual element
        cur_flattened_tensor_info = \
            flattened_tensor_infos[flattened_tensor_infos_idx[0]]
        flattened_tensor_infos_idx[0] += 1

        if cur_flattened_tensor_info is not None:
            return func(args, cur_flattened_tensor_info)
        else:
            return args
