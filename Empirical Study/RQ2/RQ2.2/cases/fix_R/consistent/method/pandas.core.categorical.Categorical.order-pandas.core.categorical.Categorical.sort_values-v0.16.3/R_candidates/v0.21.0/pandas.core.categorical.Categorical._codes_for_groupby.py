    def _codes_for_groupby(self, sort):
        """
        If sort=False, return a copy of self, coded with categories as
        returned by .unique(), followed by any categories not appearing in
        the data. If sort=True, return self.

        This method is needed solely to ensure the categorical index of the
        GroupBy result has categories in the order of appearance in the data
        (GH-8868).

        Parameters
        ----------
        sort : boolean
            The value of the sort paramter groupby was called with.

        Returns
        -------
        Categorical
            If sort=False, the new categories are set to the order of
            appearance in codes (unless ordered=True, in which case the
            original order is preserved), followed by any unrepresented
            categories in the original order.
        """

        # Already sorted according to self.categories; all is fine
        if sort:
            return self

        # sort=False should order groups in as-encountered order (GH-8868)
        cat = self.unique()

        # But for groupby to work, all categories should be present,
        # including those missing from the data (GH-13179), which .unique()
        # above dropped
        cat.add_categories(
            self.categories[~self.categories.isin(cat.categories)],
            inplace=True)

        return self.reorder_categories(cat.categories)
