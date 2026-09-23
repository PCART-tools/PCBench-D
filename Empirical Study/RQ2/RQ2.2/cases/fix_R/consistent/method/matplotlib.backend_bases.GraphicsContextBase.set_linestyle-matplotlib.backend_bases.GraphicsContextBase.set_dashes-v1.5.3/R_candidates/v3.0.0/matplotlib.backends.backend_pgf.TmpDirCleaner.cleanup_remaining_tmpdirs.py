    @staticmethod
    def cleanup_remaining_tmpdirs():
        for tmpdir in TmpDirCleaner.remaining_tmpdirs:
            shutil.rmtree(
                tmpdir,
                onerror=lambda *args: print("error deleting tmp directory %s"
                                            % tmpdir, file=sys.stderr))
