class WaitForStringPopen(subprocess.Popen):
    """
    A Popen that passes flags that allow triggering KeyboardInterrupt.
    """

    def __init__(self, *args, **kwargs):
        if sys.platform == 'win32':
            kwargs['creationflags'] = subprocess.CREATE_NEW_CONSOLE
        super().__init__(
            *args, **kwargs,
            # Force Agg so that each test can switch to its desired Qt backend.
            env={**os.environ, "MPLBACKEND": "Agg", "SOURCE_DATE_EPOCH": "0"},
            stdout=subprocess.PIPE, universal_newlines=True)

    def wait_for(self, terminator):
        """Read until the terminator is reached."""
        buf = ''
        while True:
            c = self.stdout.read(1)
            if not c:
                raise RuntimeError(
                    f'Subprocess died before emitting expected {terminator!r}')
            buf += c
            if buf.endswith(terminator):
                return
