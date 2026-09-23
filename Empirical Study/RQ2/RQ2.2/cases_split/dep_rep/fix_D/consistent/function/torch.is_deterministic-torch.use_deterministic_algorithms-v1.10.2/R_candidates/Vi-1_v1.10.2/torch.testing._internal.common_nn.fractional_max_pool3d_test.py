def fractional_max_pool3d_test(test_case):
    random_samples = torch.empty((2, 4, 3), dtype=torch.double).uniform_()
    if test_case == 'ratio':
        return dict(
            constructor=lambda: nn.FractionalMaxPool3d(
                2, output_ratio=0.5, _random_samples=random_samples),
            cpp_constructor_args='''torch::nn::FractionalMaxPool3dOptions(2)
                                    .output_ratio(0.5)
                                    ._random_samples(random_samples)''',
            input_size=(2, 4, 5, 5, 5),
            cpp_var_map={'random_samples': random_samples},
            fullname='FractionalMaxPool3d_ratio')
    elif test_case == 'size':
        return dict(
            constructor=lambda: nn.FractionalMaxPool3d((2, 2, 2), output_size=(
                4, 4, 4), _random_samples=random_samples),
            cpp_constructor_args='''torch::nn::FractionalMaxPool3dOptions({2, 2, 2})
                                    .output_size(std::vector<int64_t>({4, 4, 4}))
                                    ._random_samples(random_samples)''',
            input_size=(2, 4, 7, 7, 7),
            cpp_var_map={'random_samples': random_samples},
            fullname='FractionalMaxPool3d_size')
    elif test_case == 'asymsize':
        return dict(
            constructor=lambda: nn.FractionalMaxPool3d((4, 2, 3), output_size=(
                10, 3, 2), _random_samples=random_samples),
            cpp_constructor_args='''torch::nn::FractionalMaxPool3dOptions({4, 2, 3})
                                    .output_size(std::vector<int64_t>({10, 3, 2}))
                                    ._random_samples(random_samples)''',
            input_size=(2, 4, 16, 7, 5),
            cpp_var_map={'random_samples': random_samples},
            fullname='FractionalMaxPool3d_asymsize')
