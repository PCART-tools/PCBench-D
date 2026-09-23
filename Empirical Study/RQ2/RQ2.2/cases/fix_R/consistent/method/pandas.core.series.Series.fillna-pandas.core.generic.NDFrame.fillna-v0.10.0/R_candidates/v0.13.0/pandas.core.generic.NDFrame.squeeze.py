    def squeeze(self):
        """ squeeze length 1 dimensions """
        try:
            return self.ix[tuple([slice(None) if len(a) > 1 else a[0]
                                  for a in self.axes])]
        except:
            return self
