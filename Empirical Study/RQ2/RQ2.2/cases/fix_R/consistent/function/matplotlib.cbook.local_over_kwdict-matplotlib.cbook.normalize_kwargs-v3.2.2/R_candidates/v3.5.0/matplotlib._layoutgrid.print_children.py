def print_children(lb):
    """Print the children of the layoutbox."""
    for child in lb.children:
        print_children(child)
