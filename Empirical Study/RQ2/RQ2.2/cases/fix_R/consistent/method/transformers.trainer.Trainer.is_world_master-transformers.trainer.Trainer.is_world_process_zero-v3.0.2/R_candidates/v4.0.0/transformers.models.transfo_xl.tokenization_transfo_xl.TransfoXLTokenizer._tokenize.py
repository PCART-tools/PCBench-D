    def _tokenize(self, line, add_eos=False, add_double_eos=False):
        line = line.strip()
        # convert to lower case
        if self.lower_case:
            line = line.lower()

        # empty delimiter '' will evaluate False
        if self.delimiter == "":
            symbols = line
        else:
            symbols = self.moses_pipeline(line)

        if add_double_eos:  # lm1b
            return ["<S>"] + symbols + ["<S>"]
        elif add_eos:
            return symbols + ["<eos>"]
        else:
            return symbols
