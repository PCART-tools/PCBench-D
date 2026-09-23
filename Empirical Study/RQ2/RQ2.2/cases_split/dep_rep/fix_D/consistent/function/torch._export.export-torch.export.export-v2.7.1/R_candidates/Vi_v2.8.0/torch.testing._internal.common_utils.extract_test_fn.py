def extract_test_fn() -> Optional[Callable]:
    try:
        stack = inspect.stack()
        for frame_info in stack:
            frame = frame_info.frame
            if "self" not in frame.f_locals:
                continue
            self_val = frame.f_locals["self"]
            if isinstance(self_val, unittest.TestCase):
                test_id = self_val.id()
                test_name = test_id.split('.')[2]
                test_fn = getattr(self_val, test_name).__func__
                return test_fn
    except Exception:
        pass
    return None
