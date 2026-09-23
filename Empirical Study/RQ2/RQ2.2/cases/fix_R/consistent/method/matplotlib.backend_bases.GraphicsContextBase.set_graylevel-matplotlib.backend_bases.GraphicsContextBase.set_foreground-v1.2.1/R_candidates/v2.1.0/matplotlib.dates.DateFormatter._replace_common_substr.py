    def _replace_common_substr(self, s1, s2, sub1, sub2, replacement):
        """Helper function for replacing substrings sub1 and sub2
        located at the same indexes in strings s1 and s2 respectively,
        with the string replacement.  It is expected that sub1 and sub2
        have the same length.  Returns the pair s1, s2 after the
        substitutions.
        """
        # Find common indexes of substrings sub1 in s1 and sub2 in s2
        # and make substitutions inplace. Because this is inplace,
        # it is okay if len(replacement) != len(sub1), len(sub2).
        i = 0
        while True:
            j = s1.find(sub1, i)
            if j == -1:
                break

            i = j + 1
            if s2[j:j + len(sub2)] != sub2:
                continue

            s1 = s1[:j] + replacement + s1[j + len(sub1):]
            s2 = s2[:j] + replacement + s2[j + len(sub2):]

        return s1, s2
