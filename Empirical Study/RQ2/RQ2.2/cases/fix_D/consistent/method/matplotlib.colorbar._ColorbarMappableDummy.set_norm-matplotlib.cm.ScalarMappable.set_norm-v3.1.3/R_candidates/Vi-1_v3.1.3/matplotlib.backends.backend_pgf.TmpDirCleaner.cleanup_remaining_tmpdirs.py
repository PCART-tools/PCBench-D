    @staticmethod
    def cleanup_remaining_tmpdirs():
        for tmpdir in TmpDirCleaner.remaining_tmpdirs:
            error_message = "error deleting tmp directory {}".format(tmpdir)
            shutil.rmtree(
                tmpdir,
                onerror=lambda *args: _log.error(error_message))
