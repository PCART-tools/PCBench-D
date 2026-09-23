    def __enter__(self):
        retries = 50
        sleeptime = 0.1
        while retries:
            files = glob.glob(self.pattern)
            if files and not files[0].endswith(self.end):
                time.sleep(sleeptime)
                retries -= 1
            else:
                break
        else:
            err_str = _lockstr.format(self.pattern)
            raise self.TimeoutError(err_str)

        if not files:
            try:
                os.makedirs(self.lock_path)
            except OSError:
                pass
        else:  # PID lock already here --- someone else will remove it.
            self.remove = False
