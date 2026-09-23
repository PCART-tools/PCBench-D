def sample_inputs_rsub(op_info, device, dtype, requires_grad, variant='tensor', **kwargs):
    def _make_tensor_helper(shape, low=None, high=None):
        return make_tensor(shape, device, dtype, low=low, high=high, requires_grad=requires_grad)

    def _samples_with_alpha_helper(args, alphas, filter_fn=lambda arg_alpha: True):
        filtered_product = filter(filter_fn, product(args, alphas))  # type: ignore[var-annotated]
        return (SampleInput(input, args=(arg,), kwargs=dict(alpha=alpha))
                for (input, arg), alpha in filtered_product)

    int_alpha, float_alpha, complex_alpha = 2, 0.1, 1 + 0.6j

    if variant == 'tensor':
        samples = (
            SampleInput(_make_tensor_helper((S, S)), args=(_make_tensor_helper((S, S)),)),
            SampleInput(_make_tensor_helper((S, S)), args=(_make_tensor_helper((S,)),)),
            SampleInput(_make_tensor_helper((S,)), args=(_make_tensor_helper((S, S)),)),
            SampleInput(_make_tensor_helper(()), args=(_make_tensor_helper(()),)),
            SampleInput(_make_tensor_helper(()), args=(_make_tensor_helper((S,)),)),
            SampleInput(_make_tensor_helper((S,)), args=(_make_tensor_helper(()),)),
        )

        if dtype.is_complex:
            alphas = [int_alpha, float_alpha, complex_alpha]
        elif dtype.is_floating_point:
            alphas = [int_alpha, float_alpha]
        else:
            alphas = [int_alpha]

        args = ((_make_tensor_helper((S, S)), _make_tensor_helper((S, S))),
                (_make_tensor_helper((S, S)), _make_tensor_helper((S,))),
                (_make_tensor_helper(()), _make_tensor_helper(())))
        samples += tuple(_samples_with_alpha_helper(args, alphas))  # type: ignore[assignment]
    elif variant == 'scalar':
        # Scalar Other
        samples = (SampleInput(_make_tensor_helper((S, S)), args=(0.5,)),
                   SampleInput(_make_tensor_helper(()), args=(0.5,)),
                   SampleInput(_make_tensor_helper((S, S)), args=(1.5j,)),
                   SampleInput(_make_tensor_helper(()), args=(1.5j,)),
                   SampleInput(_make_tensor_helper((S, S)), args=(0.4 + 1.2j,)),
                   SampleInput(_make_tensor_helper(()), args=(1.2 + 1.76j,)))

        scalar_args = [(_make_tensor_helper((S, S)), 0.5), (_make_tensor_helper(()), 0.5),
                       (_make_tensor_helper((S, S)), 2.7j), (_make_tensor_helper(()), 2.7j),
                       (_make_tensor_helper((S, S)), 1 - 2.7j), (_make_tensor_helper(()), 1 + 2.7j)]

        alphas = [int_alpha, float_alpha, complex_alpha]

        def filter_fn(arg_alpha):
            arg, alpha = arg_alpha
            if isinstance(alpha, complex):
                if dtype.is_complex or isinstance(arg[1], complex):
                    return True
                else:
                    # complex alpha is valid only if either `self` or `other` is complex
                    return False

            # Non-Complex Alpha
            return True

        # Samples with alpha (scalar version) covers the following cases
        # self    | other   | alpha
        # -----------------------------------------
        # real    | real    | real (int and float)
        # real    | complex | real and complex
        # complex | real    | real and complex
        # complex | complex | real and complex
        #
        # It does not cover
        # real    | real    | complex
        # x = torch.randn(2, requires_grad=True, dtype=torch.float64)
        # torch.rsub(x, 1, alpha=1. + 1.6j)
        # RuntimeError: value cannot be converted to type double without overflow: (-1,-1.6)

        samples += tuple(_samples_with_alpha_helper(scalar_args, alphas, filter_fn=filter_fn))  # type: ignore[assignment]
    else:
        raise Exception("Invalid variant!")

    return samples
