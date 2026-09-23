    @staticmethod
    @_api.deprecated("3.4")
    @atexit.register
    def cleanup_remaining_tmpdirs():
        for tmpdir in TmpDirCleaner._remaining_tmpdirs:
            error_message = "error deleting tmp directory {}".format(tmpdir)
            shutil.rmtree(
                tmpdir,
                onerror=lambda *args: _log.error(error_message))
