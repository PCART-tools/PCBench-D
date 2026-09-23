    def get_majorticklabels(self):
        'Return a list of Text instances for the major ticklabels.'
        ticks = self.get_major_ticks()
        labels1 = [tick.label1 for tick in ticks if tick.label1.get_visible()]
        labels2 = [tick.label2 for tick in ticks if tick.label2.get_visible()]
        return cbook.silent_list('Text major ticklabel', labels1 + labels2)
