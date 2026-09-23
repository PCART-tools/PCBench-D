@contextmanager
def capture_stdout() -> Generator[Callable[[], str], None, None]:
  with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as fp:
    def _read() -> str:
      return fp.getvalue()
    yield _read
