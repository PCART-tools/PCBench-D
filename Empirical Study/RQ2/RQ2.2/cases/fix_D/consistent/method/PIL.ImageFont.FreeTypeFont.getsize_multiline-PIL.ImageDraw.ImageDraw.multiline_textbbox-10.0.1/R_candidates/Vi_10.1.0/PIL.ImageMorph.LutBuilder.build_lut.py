    def build_lut(self):
        """Compile all patterns into a morphology lut.

        TBD :Build based on (file) morphlut:modify_lut
        """
        self.build_default_lut()
        patterns = []

        # Parse and create symmetries of the patterns strings
        for p in self.patterns:
            m = re.search(r"(\w*):?\s*\((.+?)\)\s*->\s*(\d)", p.replace("\n", ""))
            if not m:
                msg = 'Syntax error in pattern "' + p + '"'
                raise Exception(msg)
            options = m.group(1)
            pattern = m.group(2)
            result = int(m.group(3))

            # Get rid of spaces
            pattern = pattern.replace(" ", "").replace("\n", "")

            patterns += self._pattern_permute(pattern, options, result)

        # compile the patterns into regular expressions for speed
        for i, pattern in enumerate(patterns):
            p = pattern[0].replace(".", "X").replace("X", "[01]")
            p = re.compile(p)
            patterns[i] = (p, pattern[1])

        # Step through table and find patterns that match.
        # Note that all the patterns are searched. The last one
        # caught overrides
        for i in range(LUT_SIZE):
            # Build the bit pattern
            bitpattern = bin(i)[2:]
            bitpattern = ("0" * (9 - len(bitpattern)) + bitpattern)[::-1]

            for p, r in patterns:
                if p.match(bitpattern):
                    self.lut[i] = [0, 1][r]

        return self.lut
