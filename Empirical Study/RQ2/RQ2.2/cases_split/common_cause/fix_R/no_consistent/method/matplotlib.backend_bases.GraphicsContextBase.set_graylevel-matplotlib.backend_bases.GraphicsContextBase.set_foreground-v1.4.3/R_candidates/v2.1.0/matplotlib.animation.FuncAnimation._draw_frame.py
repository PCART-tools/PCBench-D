    def _draw_frame(self, framedata):
        # Save the data for potential saving of movies.
        self._save_seq.append(framedata)

        # Make sure to respect save_count (keep only the last save_count
        # around)
        self._save_seq = self._save_seq[-self.save_count:]

        # Call the func with framedata and args. If blitting is desired,
        # func needs to return a sequence of any artists that were modified.
        self._drawn_artists = self._func(framedata, *self._args)
        if self._blit:
            if self._drawn_artists is None:
                    raise RuntimeError('The animation function must return a '
                                       'sequence of Artist objects.')
            for a in self._drawn_artists:
                a.set_animated(self._blit)
