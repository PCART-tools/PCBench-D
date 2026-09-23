    def __init__(self, filename):
        self._font = {}
        self._filename = filename
        if six.PY3 and isinstance(filename, bytes):
            encoding = sys.getfilesystemencoding() or 'utf-8'
            self._filename = filename.decode(encoding, errors='replace')
        with open(filename, 'rb') as file:
            self._parse(file)
