    def load(self, file_path):
        file_path = pathlib.Path(file_path)
        with file_path.open(mode='rb') as f:
            self._cookies = pickle.load(f)
