    def get_minorticklabels(self):
        'Return a list of Text instances for the minor ticklabels.'
        ticks = self.get_minor_ticks()
        labels1 = [tick.label1 for tick in ticks if tick.label1.get_visible()]
        labels2 = [tick.label2 for tick in ticks if tick.label2.get_visible()]
        return cbook.silent_list('Text minor ticklabel', labels1 + labels2)
