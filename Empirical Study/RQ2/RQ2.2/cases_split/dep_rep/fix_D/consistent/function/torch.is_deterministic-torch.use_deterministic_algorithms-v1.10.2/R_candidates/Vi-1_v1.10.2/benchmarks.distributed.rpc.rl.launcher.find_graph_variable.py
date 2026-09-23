def find_graph_variable(args):
    r"""
    Determines if user specified multiple entries for a single argument, in which case
    benchmark is run for each of these entries.  Comma separated values in a given argument indicate multiple entries.
    Output is presented so that user can use plot repo to plot the results with each of the
    variable argument's entries on the x-axis. Args is modified in accordance with this.
    More than 1 argument with multiple entries is not permitted.
    Args:
        args (dict): Dictionary containing arguments passed by the user (and default arguments)
    """
    var_types = {'world_size': int,
                 'state_size': str,
                 'nlayers': int,
                 'out_features': int,
                 'batch': str2bool}
    for arg in var_types.keys():
        if ',' in args[arg]:
            if args.get('x_axis_name'):
                raise("Only 1 x axis graph variable allowed")
            args[arg] = list(map(var_types[arg], args[arg].split(',')))  # convert , separated str to list
            args['x_axis_name'] = arg
        else:
            args[arg] = var_types[arg](args[arg])  # convert string to proper type
