    def save(self, file_path):
        file_path = pathlib.Path(file_path)
        with file_path.open(mode='wb') as f:
            pickle.dump(self._cookies, f, pickle.HIGHEST_PROTOCOL)
