    def get_auto_remove_tmp_dir(self, tmp_dir=None, after=True, before=False):
        """
        Args:
            tmp_dir (:obj:`string`, `optional`):
                use this path, if None a unique path will be assigned
            before (:obj:`bool`, `optional`, defaults to :obj:`False`):
                if `True` and tmp dir already exists make sure to empty it right away
            after (:obj:`bool`, `optional`, defaults to :obj:`True`):
                delete the tmp dir at the end of the test

        Returns:
            tmp_dir(:obj:`string`): either the same value as passed via `tmp_dir` or the path to the auto-created tmp
            dir
        """
        if tmp_dir is not None:
            # using provided path
            path = Path(tmp_dir).resolve()

            # to avoid nuking parts of the filesystem, only relative paths are allowed
            if not tmp_dir.startswith("./"):
                raise ValueError(
                    f"`tmp_dir` can only be a relative path, i.e. `./some/path`, but received `{tmp_dir}`"
                )

            # ensure the dir is empty to start with
            if before is True and path.exists():
                shutil.rmtree(tmp_dir, ignore_errors=True)

            path.mkdir(parents=True, exist_ok=True)

        else:
            # using unique tmp dir (always empty, regardless of `before`)
            tmp_dir = tempfile.mkdtemp()

        if after is True:
            # register for deletion
            self.teardown_tmp_dirs.append(tmp_dir)

        return tmp_dir
