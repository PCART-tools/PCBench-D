def _decide_input_format(model, args):
    import inspect
    try:
        sig = inspect.signature(model.forward)
        ordered_list_keys = list(sig.parameters.keys())
        if isinstance(args[-1], dict):
            args_dict = args[-1]
            args = list(args)[:-1]
            n_nonkeyword = len(args)
            for optional_arg in ordered_list_keys[n_nonkeyword:]:
                if optional_arg in args_dict:
                    args.append(args_dict[optional_arg])
                # Check if this arg has a default value
                else:
                    param = sig.parameters[optional_arg]
                    if param.default is param.empty:
                        args.append(None)
                    else:
                        args.append(param.default)
            args = tuple(args)
        return args
    # Cases of models without forward functions and dict inputs
    except (AttributeError, ValueError):
        warnings.warn("Model has no forward function")
        return args
    # Cases of models with no input args
    except IndexError:
        warnings.warn("No input args")
        return args
    except Exception as e:
        warnings.warn("Skipping _decide_input_format\n {}".format(e.args[0]))
        return args
