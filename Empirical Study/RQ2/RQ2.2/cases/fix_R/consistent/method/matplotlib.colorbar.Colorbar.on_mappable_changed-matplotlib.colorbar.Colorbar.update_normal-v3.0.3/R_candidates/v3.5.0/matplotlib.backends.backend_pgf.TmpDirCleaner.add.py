    @staticmethod
    @_api.deprecated("3.4")
    def add(tmpdir):
        TmpDirCleaner._remaining_tmpdirs.add(tmpdir)
