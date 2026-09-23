    def legend_elements(self, variable_name='x', str_format=str):
        """
        Return a list of artists and labels suitable for passing through
        to `~.Axes.legend` which represent this ContourSet.

        The labels have the form "0 < x <= 1" stating the data ranges which
        the artists represent.

        Parameters
        ----------
        variable_name : str
            The string used inside the inequality used on the labels.

        str_format : function: float -> str
            Function used to format the numbers in the labels.

        Returns
        -------
        artists : List[`.Artist`]
            A list of the artists.

        labels : List[str]
            A list of the labels.

        """
        artists = []
        labels = []

        if self.filled:
            lowers, uppers = self._get_lowers_and_uppers()
            n_levels = len(self.collections)

            for i, (collection, lower, upper) in enumerate(
                    zip(self.collections, lowers, uppers)):
                patch = mpatches.Rectangle(
                    (0, 0), 1, 1,
                    facecolor=collection.get_facecolor()[0],
                    hatch=collection.get_hatch(),
                    alpha=collection.get_alpha())
                artists.append(patch)

                lower = str_format(lower)
                upper = str_format(upper)

                if i == 0 and self.extend in ('min', 'both'):
                    labels.append(fr'${variable_name} \leq {lower}s$')
                elif i == n_levels - 1 and self.extend in ('max', 'both'):
                    labels.append(fr'${variable_name} > {upper}s$')
                else:
                    labels.append(fr'${lower} < {variable_name} \leq {upper}$')
        else:
            for collection, level in zip(self.collections, self.levels):

                patch = mcoll.LineCollection(None)
                patch.update_from(collection)

                artists.append(patch)
                # format the level for insertion into the labels
                level = str_format(level)
                labels.append(fr'${variable_name} = {level}$')

        return artists, labels
