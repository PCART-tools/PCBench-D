    def _find_tails(self, mag, rounding=True, half=5, full=10, flag=50):
        '''
        Find how many of each of the tail pieces is necessary.  Flag
        specifies the increment for a flag, barb for a full barb, and half for
        half a barb. Mag should be the magnitude of a vector (i.e., >= 0).

        This returns a tuple of:

            (*number of flags*, *number of barbs*, *half_flag*, *empty_flag*)

        *half_flag* is a boolean whether half of a barb is needed,
        since there should only ever be one half on a given
        barb. *empty_flag* flag is an array of flags to easily tell if
        a barb is empty (too low to plot any barbs/flags.
        '''

        # If rounding, round to the nearest multiple of half, the smallest
        # increment
        if rounding:
            mag = half * (mag / half + 0.5).astype(int)

        num_flags = np.floor(mag / flag).astype(int)
        mag = np.mod(mag, flag)

        num_barb = np.floor(mag / full).astype(int)
        mag = np.mod(mag, full)

        half_flag = mag >= half
        empty_flag = ~(half_flag | (num_flags > 0) | (num_barb > 0))

        return num_flags, num_barb, half_flag, empty_flag
