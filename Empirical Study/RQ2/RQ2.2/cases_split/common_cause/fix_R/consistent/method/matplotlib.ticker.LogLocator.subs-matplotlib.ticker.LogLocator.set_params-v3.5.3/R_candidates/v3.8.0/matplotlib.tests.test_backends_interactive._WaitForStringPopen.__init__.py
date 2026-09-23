    def __init__(self, *args, **kwargs):
        if sys.platform == 'win32':
            kwargs['creationflags'] = subprocess.CREATE_NEW_CONSOLE
        super().__init__(
            *args, **kwargs,
            # Force Agg so that each test can switch to its desired backend.
            env={**os.environ, "MPLBACKEND": "Agg", "SOURCE_DATE_EPOCH": "0"},
            stdout=subprocess.PIPE, universal_newlines=True)
