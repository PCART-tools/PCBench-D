    def url_for(self, *, filename, append_version=None):
        if append_version is None:
            append_version = self._append_version
        if isinstance(filename, Path):
            filename = str(filename)
        while filename.startswith('/'):
            filename = filename[1:]
        filename = '/' + filename
        url = self._prefix + URL(filename).raw_path
        url = URL(url)
        if append_version is True:
            try:
                if filename.startswith('/'):
                    filename = filename[1:]
                filepath = self._directory.joinpath(filename).resolve()
                if not self._follow_symlinks:
                    filepath.relative_to(self._directory)
            except (ValueError, FileNotFoundError):
                # ValueError for case when path point to symlink
                # with follow_symlinks is False
                return url  # relatively safe
            if filepath.is_file():
                # TODO cache file content
                # with file watcher for cache invalidation
                with open(str(filepath), mode='rb') as f:
                    file_bytes = f.read()
                h = self._get_file_hash(file_bytes)
                url = url.with_query({self.VERSION_KEY: h})
                return url
        return url
