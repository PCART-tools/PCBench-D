    def _compile_space_around_punctuation_pattern(self):
        look_ahead_for_special_token = "(?=[{}])".format(self.punctuation_symbols)
        look_ahead_to_match_all_except_space = r"(?=[^\s])"
        return re.compile(r"" + look_ahead_for_special_token + look_ahead_to_match_all_except_space)
