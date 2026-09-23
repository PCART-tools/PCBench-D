    def __del__(self):
        if self._proc:
            if self._proc.poll() is None:  # Not exited yet.
                self._proc.communicate(b"quit\n")
                self._proc.wait()
            self._proc.stdin.close()
            self._proc.stdout.close()
            self._stderr.close()
