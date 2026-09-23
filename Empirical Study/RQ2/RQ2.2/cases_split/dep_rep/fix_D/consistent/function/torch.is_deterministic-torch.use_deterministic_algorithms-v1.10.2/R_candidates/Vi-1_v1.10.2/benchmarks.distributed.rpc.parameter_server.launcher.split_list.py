def split_list(arr, n):
    r"""
    A function that splits a list into n lists
    Args:
        arr (list): training samples
        n (int): number of output lists
    """
    return [arr[i::n] for i in range(n)]
