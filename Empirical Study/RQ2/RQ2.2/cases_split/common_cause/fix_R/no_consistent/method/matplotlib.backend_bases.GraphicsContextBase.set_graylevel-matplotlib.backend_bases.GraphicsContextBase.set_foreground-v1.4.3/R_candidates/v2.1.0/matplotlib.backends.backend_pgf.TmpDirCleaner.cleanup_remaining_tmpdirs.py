    @staticmethod
    def cleanup_remaining_tmpdirs():
        for tmpdir in TmpDirCleaner.remaining_tmpdirs:
            try:
                shutil.rmtree(tmpdir)
            except:
                sys.stderr.write("error deleting tmp directory %s\n" % tmpdir)
