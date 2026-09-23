def get_all_call_args(call_args_list, arg_types_list):
    """
    Passed in the call_args for each subkernel and return the call_args for the
    combined multi-kernel.

    Note an algorithm as follows does not always work:
    ```
        all_call_args: Dict[
            Any, None
        ] = {}  # use a dict rather than set to maintain insertion order
        for call_args in call_args_list:
            all_call_args.update({arg: None for arg in call_args})

        all_call_args = list(all_call_args.keys())
    ```
    It will fail if any kernel has the same argument passed in multiple times.
    Check test_pass_same_arg_multi_times in test_multi_kernel.py

    Instead, we pick the longest call args and assert that other call args are
    a subset of it.
    """
    return _get_all_args(call_args_list, arg_types_list)
