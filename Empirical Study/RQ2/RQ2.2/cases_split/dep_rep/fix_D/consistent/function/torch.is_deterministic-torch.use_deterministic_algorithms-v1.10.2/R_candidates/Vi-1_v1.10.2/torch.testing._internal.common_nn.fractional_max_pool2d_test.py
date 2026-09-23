def fractional_max_pool2d_test(test_case):
    random_samples = torch.empty((1, 3, 2), dtype=torch.double).uniform_()
    if test_case == 'ratio':
        return dict(
            constructor=lambda: nn.FractionalMaxPool2d(
                2, output_ratio=0.5, _random_samples=random_samples),
            cpp_constructor_args='''torch::nn::FractionalMaxPool2dOptions(2)
                                    .output_ratio(0.5)
                                    ._random_samples(random_samples)''',
            input_size=(1, 3, 5, 7),
            cpp_var_map={'random_samples': random_samples},
            fullname='FractionalMaxPool2d_ratio')
    elif test_case == 'size':
        return dict(
            constructor=lambda: nn.FractionalMaxPool2d((2, 3), output_size=(
                4, 3), _random_samples=random_samples),
            cpp_constructor_args='''torch::nn::FractionalMaxPool2dOptions({2, 3})
                                    .output_size(std::vector<int64_t>({4, 3}))
                                    ._random_samples(random_samples)''',
            input_size=(1, 3, 7, 6),
            cpp_var_map={'random_samples': random_samples},
            fullname='FractionalMaxPool2d_size')
