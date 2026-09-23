def fractional_max_pool3d_no_batch_dim_test(test_case, use_random_samples):
    if use_random_samples:
        # random_samples enables CPU and GPU checks to be consistent
        random_samples = torch.empty((2, 4, 3), dtype=torch.double).uniform_()
        if test_case == 'ratio':
            return dict(
                constructor=lambda: nn.FractionalMaxPool3d(
                    2, output_ratio=0.5, _random_samples=random_samples),
                cpp_constructor_args='''torch::nn::FractionalMaxPool3dOptions(2)
                                        .output_ratio(0.5)
                                        ._random_samples(random_samples)''',
                input_size=(4, 5, 5, 5),
                cpp_var_map={'random_samples': random_samples},
                reference_fn=single_batch_reference_fn,
                fullname='FractionalMaxPool3d_ratio_no_batch_dim')
        elif test_case == 'size':
            return dict(
                constructor=lambda: nn.FractionalMaxPool3d((2, 2, 2), output_size=(
                    4, 4, 4), _random_samples=random_samples),
                cpp_constructor_args='''torch::nn::FractionalMaxPool3dOptions({2, 2, 2})
                                        .output_size(std::vector<int64_t>({4, 4, 4}))
                                        ._random_samples(random_samples)''',
                input_size=(4, 7, 7, 7),
                cpp_var_map={'random_samples': random_samples},
                reference_fn=single_batch_reference_fn,
                fullname='FractionalMaxPool3d_size_no_batch_dim')
    else:
        # can not check cuda because there RNG is different between cpu and cuda
        if test_case == 'ratio':
            return dict(
                constructor=lambda: nn.FractionalMaxPool3d(
                    2, output_ratio=0.5),
                cpp_constructor_args='''torch::nn::FractionalMaxPool3dOptions(2)
                                        .output_ratio(0.5)''',
                input_size=(4, 5, 5, 5),
                reference_fn=single_batch_reference_fn,
                test_cuda=False,
                fullname='FractionalMaxPool3d_ratio_no_batch_dim_no_random_samples')
        elif test_case == 'size':
            return dict(
                constructor=lambda: nn.FractionalMaxPool3d((2, 2, 2), output_size=(
                    4, 4, 4)),
                cpp_constructor_args='''torch::nn::FractionalMaxPool3dOptions({2, 2, 2})
                                        .output_size(std::vector<int64_t>({4, 4, 4}))''',
                input_size=(4, 7, 7, 7),
                reference_fn=single_batch_reference_fn,
                test_cuda=False,
                fullname='FractionalMaxPool3d_size_no_batch_dim_no_random_samples')
