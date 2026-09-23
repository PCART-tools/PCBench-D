    def _sendfile_cb(self, fut, out_fd, in_fd,
                     offset, count, loop, registered):
        if registered:
            loop.remove_writer(out_fd)
        if fut.cancelled():
            return

        try:
            n = os.sendfile(out_fd, in_fd, offset, count)
            if n == 0:  # EOF reached
                n = count
        except (BlockingIOError, InterruptedError):
            n = 0
        except Exception as exc:
            set_exception(fut, exc)
            return

        if n < count:
            loop.add_writer(out_fd, self._sendfile_cb, fut, out_fd, in_fd,
                            offset + n, count - n, loop, True)
        else:
            set_result(fut, None)
