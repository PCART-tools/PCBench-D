    def _format_footer(self):
        tagline = 'Length: %d, Freq: %s, Timezone: %s'
        return tagline % (len(self), self.freqstr, self.tz)
