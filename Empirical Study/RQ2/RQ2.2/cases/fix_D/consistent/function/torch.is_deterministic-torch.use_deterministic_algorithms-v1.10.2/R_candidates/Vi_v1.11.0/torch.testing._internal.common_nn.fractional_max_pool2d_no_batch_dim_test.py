def fractional_max_pool2d_no_batch_dim_test(test_case, use_random_samples):
    if use_random_samples:
        # random_samples enables CPU and GPU checks to be consistent
        random_samples = torch.empty((1, 3, 2), dtype=torch.double).uniform_()
        if test_case == 'ratio':
            return dict(
                constructor=lambda: nn.FractionalMaxPool2d(
                    2, output_ratio=0.5, _random_samples=random_samples),
                cpp_constructor_args='''torch::nn::FractionalMaxPool2dOptions(2)
                                        .output_ratio(0.5)
                                        ._random_samples(random_samples)''',
                input_size=(3, 5, 7),
                cpp_var_map={'random_samples': random_samples},
                reference_fn=single_batch_reference_fn,
                fullname='FractionalMaxPool2d_ratio_no_batch_dim')
        elif test_case == 'size':
            return dict(
                constructor=lambda: nn.FractionalMaxPool2d((2, 3), output_size=(
                    4, 3), _random_samples=random_samples),
                cpp_constructor_args='''torch::nn::FractionalMaxPool2dOptions({2, 3})
                                        .output_size(std::vector<int64_t>({4, 3}))
                                        ._random_samples(random_samples)''',
                input_size=(3, 7, 6),
                cpp_var_map={'random_samples': random_samples},
                reference_fn=single_batch_reference_fn,
                fullname='FractionalMaxPool2d_size_no_batch_dim')
    else:
        # can not check cuda because there RNG is different between cpu and cuda
        if test_case == 'ratio':
            return dict(
                constructor=lambda: nn.FractionalMaxPool2d(
                    2, output_ratio=0.5),
                cpp_constructor_args='''torch::nn::FractionalMaxPool2dOptions(2)
                                        .output_ratio(0.5)''',
                input_size=(3, 5, 7),
                reference_fn=single_batch_reference_fn,
                test_cuda=False,
                fullname='FractionalMaxPool2d_ratio_no_batch_dim_no_random_samples')
        elif test_case == 'size':
            return dict(
                constructor=lambda: nn.FractionalMaxPool2d((2, 3), output_size=(
                    4, 3)),
                cpp_constructor_args='''torch::nn::FractionalMaxPool2dOptions({2, 3})
                                        .output_size(std::vector<int64_t>({4, 3}))''',
                input_size=(3, 7, 6),
                reference_fn=single_batch_reference_fn,
                test_cuda=False,
                fullname='FractionalMaxPool2d_size_no_batch_dim_no_random_samples')
