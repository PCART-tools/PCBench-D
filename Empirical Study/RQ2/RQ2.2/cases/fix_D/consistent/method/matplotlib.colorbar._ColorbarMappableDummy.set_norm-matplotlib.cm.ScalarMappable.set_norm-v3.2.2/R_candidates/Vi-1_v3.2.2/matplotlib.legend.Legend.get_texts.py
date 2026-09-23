    def get_texts(self):
        'Return a list of `~.text.Text` instances in the legend.'
        return silent_list('Text', self.texts)
