    @cache_readonly
    def result_index(self):
        if self.all_grouper is not None:
            all_categories = self.all_grouper.categories

            # we re-order to the original category orderings
            if self.sort:
                return self.group_index.set_categories(all_categories)

            # we are not sorting, so add unobserved to the end
            categories = self.group_index.categories
            return self.group_index.add_categories(
                all_categories[~all_categories.isin(categories)])

        return self.group_index
