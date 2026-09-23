def _count_lu_permutations(perm_array):
    """Counts the number of permutations in SuperLU perm_c or perm_r"""
    perm_cnt = 0
    arr = perm_array.tolist()
    for i in range(len(arr)):
        if i != arr[i]:
            perm_cnt += 1
            n = arr.index(i)
            arr[n] = arr[i]
            arr[i] = i

    return perm_cnt
