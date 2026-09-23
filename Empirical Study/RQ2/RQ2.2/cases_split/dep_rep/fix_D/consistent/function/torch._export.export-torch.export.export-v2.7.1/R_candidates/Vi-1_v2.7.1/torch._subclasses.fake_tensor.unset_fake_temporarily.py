@contextlib.contextmanager
def unset_fake_temporarily() -> Generator[Optional[TorchDispatchMode], None, None]:
    old = torch._C._unset_dispatch_mode(torch._C._TorchDispatchModeKey.FAKE)
    try:
        yield old
    finally:
        if old is not None:
            torch._C._set_dispatch_mode(old)
