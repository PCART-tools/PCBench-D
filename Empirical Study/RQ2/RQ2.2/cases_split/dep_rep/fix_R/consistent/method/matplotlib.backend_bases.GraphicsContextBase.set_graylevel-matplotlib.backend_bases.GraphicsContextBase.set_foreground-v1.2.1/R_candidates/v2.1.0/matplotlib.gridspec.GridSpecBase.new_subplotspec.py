    def new_subplotspec(self, loc, rowspan=1, colspan=1):
        """
        create and return a SuplotSpec instance.
        """
        loc1, loc2 = loc
        subplotspec = self[loc1:loc1+rowspan, loc2:loc2+colspan]
        return subplotspec
