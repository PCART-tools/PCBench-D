def index(iterator, item, start=0, end=None):
    from itertools import islice

    for i, elem in islice(enumerate(iterator), start, end):
        if item == elem:
            return i
    # This will not run in dynamo
    raise ValueError(f"{item} is not in {type(iterator)}")
