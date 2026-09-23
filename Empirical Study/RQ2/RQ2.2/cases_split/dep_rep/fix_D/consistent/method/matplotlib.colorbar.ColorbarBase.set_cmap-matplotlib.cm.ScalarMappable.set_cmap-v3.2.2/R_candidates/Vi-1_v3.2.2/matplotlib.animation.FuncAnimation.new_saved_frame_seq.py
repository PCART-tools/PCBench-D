    def new_saved_frame_seq(self):
        # Generate an iterator for the sequence of saved data. If there are
        # no saved frames, generate a new frame sequence and take the first
        # save_count entries in it.
        if self._save_seq:
            # While iterating we are going to update _save_seq
            # so make a copy to safely iterate over
            self._old_saved_seq = list(self._save_seq)
            return iter(self._old_saved_seq)
        else:
            if self.save_count is not None:
                return itertools.islice(self.new_frame_seq(), self.save_count)

            else:
                frame_seq = self.new_frame_seq()

                def gen():
                    try:
                        for _ in range(100):
                            yield next(frame_seq)
                    except StopIteration:
                        pass
                    else:
                        cbook.warn_deprecated(
                            "2.2", message="FuncAnimation.save has truncated "
                            "your animation to 100 frames.  In the future, no "
                            "such truncation will occur; please pass "
                            "'save_count' accordingly.")

                return gen()
