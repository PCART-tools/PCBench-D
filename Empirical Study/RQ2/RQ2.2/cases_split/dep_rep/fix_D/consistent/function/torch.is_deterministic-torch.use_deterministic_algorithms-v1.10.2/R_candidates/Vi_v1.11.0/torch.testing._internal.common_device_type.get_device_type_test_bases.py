def get_device_type_test_bases():
    # set type to List[Any] due to mypy list-of-union issue:
    # https://github.com/python/mypy/issues/3351
    test_bases: List[Any] = list()

    if IS_SANDCASTLE or IS_FBCODE:
        if IS_REMOTE_GPU:
            # Skip if sanitizer is enabled
            if not TEST_WITH_ASAN and not TEST_WITH_TSAN and not TEST_WITH_UBSAN:
                test_bases.append(CUDATestBase)
        else:
            test_bases.append(CPUTestBase)
            test_bases.append(MetaTestBase)
    else:
        test_bases.append(CPUTestBase)
        if not TEST_SKIP_NOARCH:
            test_bases.append(MetaTestBase)
        if torch.cuda.is_available():
            test_bases.append(CUDATestBase)

    return test_bases
