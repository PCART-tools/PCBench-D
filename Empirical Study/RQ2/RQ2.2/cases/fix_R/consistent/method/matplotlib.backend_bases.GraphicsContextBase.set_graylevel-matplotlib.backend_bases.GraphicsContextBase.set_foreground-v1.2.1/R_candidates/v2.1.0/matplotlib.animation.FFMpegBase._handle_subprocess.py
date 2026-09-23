    @classmethod
    def _handle_subprocess(cls, process):
        _, err = process.communicate()
        # Ubuntu 12.04 ships a broken ffmpeg binary which we shouldn't use
        # NOTE : when removed, remove the same method in AVConvBase.
        if 'Libav' in err.decode():
            return False
        return True
