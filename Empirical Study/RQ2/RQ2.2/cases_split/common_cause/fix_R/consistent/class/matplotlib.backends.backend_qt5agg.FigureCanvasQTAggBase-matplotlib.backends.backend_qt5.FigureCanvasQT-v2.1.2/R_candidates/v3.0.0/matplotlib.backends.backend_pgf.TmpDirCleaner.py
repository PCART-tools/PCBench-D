class TmpDirCleaner:
    remaining_tmpdirs = set()

    @staticmethod
    def add(tmpdir):
        TmpDirCleaner.remaining_tmpdirs.add(tmpdir)

    @staticmethod
    def cleanup_remaining_tmpdirs():
        for tmpdir in TmpDirCleaner.remaining_tmpdirs:
            shutil.rmtree(
                tmpdir,
                onerror=lambda *args: print("error deleting tmp directory %s"
                                            % tmpdir, file=sys.stderr))
