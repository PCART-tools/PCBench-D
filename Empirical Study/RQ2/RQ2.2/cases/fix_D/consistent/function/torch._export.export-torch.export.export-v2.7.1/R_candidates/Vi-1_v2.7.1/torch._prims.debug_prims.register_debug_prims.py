def register_debug_prims():
    torch.library.define(
        "debugprims::load_tensor",
        "(str name, int[] size, int[] stride, *, ScalarType dtype, Device device) -> Tensor",
    )

    @torch.library.impl("debugprims::load_tensor", "BackendSelect")
    def load_tensor_factory(name, size, stride, dtype, device):
        if LOAD_TENSOR_READER is None:
            from torch._dynamo.testing import rand_strided

            return rand_strided(size, stride, dtype, device)
        else:
            from torch._dynamo.utils import clone_input

            # device argument here takes care of coercion
            r = LOAD_TENSOR_READER.read_tensor(name, device=device)
            assert list(r.size()) == size, f"{r.size()} != {size}"
            assert list(r.stride()) == stride, f"{r.stride()} != {stride}"
            assert r.device == device, f"{r.device} != {device}"

            # Unlike the other properties, we will do coercions for dtype
            # mismatch
            if r.dtype != dtype:
                r = clone_input(r, dtype=dtype)
            return r
