@contextmanager
def parametrize(*, use_const_ref_for_mutable_tensors: bool) -> Iterator[None]:
    old_use_const_ref_for_mutable_tensors = _locals.use_const_ref_for_mutable_tensors
    try:
        _locals.use_const_ref_for_mutable_tensors = use_const_ref_for_mutable_tensors
        yield
    finally:
        _locals.use_const_ref_for_mutable_tensors = old_use_const_ref_for_mutable_tensors
