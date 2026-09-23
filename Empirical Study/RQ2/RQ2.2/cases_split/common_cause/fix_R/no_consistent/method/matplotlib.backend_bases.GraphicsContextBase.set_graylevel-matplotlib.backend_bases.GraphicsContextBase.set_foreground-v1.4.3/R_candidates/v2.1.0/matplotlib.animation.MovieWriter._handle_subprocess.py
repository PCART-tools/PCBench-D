    @classmethod
    def _handle_subprocess(cls, process):
        process.communicate()
        return True
