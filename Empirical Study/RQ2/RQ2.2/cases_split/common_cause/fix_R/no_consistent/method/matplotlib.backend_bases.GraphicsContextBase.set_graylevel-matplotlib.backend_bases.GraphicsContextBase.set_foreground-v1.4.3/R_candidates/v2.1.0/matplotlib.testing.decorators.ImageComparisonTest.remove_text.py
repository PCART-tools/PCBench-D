    @staticmethod
    @cbook.deprecated('2.1',
                      alternative='remove_ticks_and_titles')
    def remove_text(figure):
        remove_ticks_and_titles(figure)
