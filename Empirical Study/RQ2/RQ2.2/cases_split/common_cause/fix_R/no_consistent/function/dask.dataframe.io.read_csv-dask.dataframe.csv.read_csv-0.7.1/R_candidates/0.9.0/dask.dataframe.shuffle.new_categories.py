def new_categories(categories, index):
    """ Flop around index for '.index' """
    if index in categories:
        categories = categories.copy()
        categories['.index'] = categories.pop(index)
    return categories
