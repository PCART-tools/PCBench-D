def skipIfRocmArch(arch: tuple[str, ...]):
    def dec_fn(fn):
        @wraps(fn)
        def wrap_fn(self, *args, **kwargs):
            if TEST_WITH_ROCM:
                prop = torch.cuda.get_device_properties(0)
                if prop.gcnArchName.split(":")[0] in arch:
                    reason = f"skipIfRocm: test skipped on {arch}"
                    raise unittest.SkipTest(reason)
            return fn(self, *args, **kwargs)
        return wrap_fn
    return dec_fn
