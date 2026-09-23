def generate_not_implemented_tests(cls):
    class UnknownType:
        pass

    # TODO: refactor to inline these
    _types = [
        torch.half, torch.float, torch.double,
        torch.int8, torch.short, torch.int, torch.long,
        torch.uint8
    ]

    # TODO: refactor to use make_tensor
    def _small_2d(dtype, device, has_zeros=True, fill_ones=False, oneish=False):
        t = _make_tensor((5, 5), dtype, device, fill_ones=fill_ones)
        if oneish:
            return t.clamp(min=_number(.99, 1, dtype), max=1.01)
        if not has_zeros:
            return t.clamp(min=(_number(_div_min, 1, dtype)))
        return t

    def create_test_func(op):
        @dtypes(*_types)
        def test(self, device, dtype):
            # Generate the inputs
            tensor = _small_2d(dtype, device)

            # Runs the tensor op on the device
            result = getattr(tensor, op)(UnknownType())
            self.assertEqual(result, NotImplemented)
        return test

    for op in tensor_binary_ops:
        test_name = "test_{}_not_implemented".format(op)
        assert not hasattr(cls, test_name), "{0} already in {1}".format(
            test_name, cls.__name__)

        setattr(cls, test_name, create_test_func(op))
