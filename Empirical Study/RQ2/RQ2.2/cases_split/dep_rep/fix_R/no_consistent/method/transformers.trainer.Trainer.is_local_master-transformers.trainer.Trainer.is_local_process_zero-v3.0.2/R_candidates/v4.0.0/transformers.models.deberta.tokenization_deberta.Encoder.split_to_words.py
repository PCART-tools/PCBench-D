    def split_to_words(self, text):
        return list(re.findall(self.pat, text))
