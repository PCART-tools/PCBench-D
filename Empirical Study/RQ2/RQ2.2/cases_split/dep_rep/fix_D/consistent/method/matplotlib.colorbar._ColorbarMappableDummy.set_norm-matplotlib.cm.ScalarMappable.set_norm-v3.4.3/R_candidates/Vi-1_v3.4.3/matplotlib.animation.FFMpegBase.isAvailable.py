    @classmethod
    def isAvailable(cls):
        return (
            super().isAvailable()
            # Ubuntu 12.04 ships a broken ffmpeg binary which we shouldn't use.
            # NOTE: when removed, remove the same method in AVConvBase.
            and b'LibAv' not in subprocess.run(
                [cls.bin_path()], creationflags=subprocess_creation_flags,
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE).stderr)
