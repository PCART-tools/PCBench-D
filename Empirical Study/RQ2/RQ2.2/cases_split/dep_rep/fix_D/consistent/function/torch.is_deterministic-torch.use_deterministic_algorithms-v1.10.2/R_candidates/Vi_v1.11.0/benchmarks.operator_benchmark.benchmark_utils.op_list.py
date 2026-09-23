def op_list(**configs):
    """Generate a list of ops organized in a specific format.
       It takes two parameters which are "attr_names" and "attr".
       attrs stores the name and function of operators.
       Args:
           configs: key-value pairs including the name and function of
           operators. attrs and attr_names must be present in configs.
       Return:
           a sequence of dictionaries which stores the name and function
           of ops in a specifal format
       Example:
       attrs = [
           ["abs", torch.abs],
           ["abs_", torch.abs_],
       ]
       attr_names = ["op_name", "op"].

       With those two examples,
       we will generate (({"op_name": "abs"}, {"op" : torch.abs}),
                         ({"op_name": "abs_"}, {"op" : torch.abs_}))
    """
    generated_configs = []
    if "attrs" not in configs:
        raise ValueError("Missing attrs in configs")
    for inputs in configs["attrs"]:
        tmp_result = {configs["attr_names"][i] : input_value
                      for i, input_value in enumerate(inputs)}
        generated_configs.append(tmp_result)
    return generated_configs
