def PrintTrie(trie, prefix, max_depth, min_size, color):
    """Prints the symbol trie in a readable manner.
    """
    if len(trie.name) == max_depth or not trie.dictionary.keys():
        # If we are reaching a leaf node or the maximum depth, we will print the
        # result.
        if trie.size > min_size:
            print('{0}{1} {2}'.format(
                  prefix,
                  MaybeAddColor(trie.name, color),
                  ReadableSize(trie.size)))
    elif len(trie.dictionary.keys()) == 1:
        # There is only one child in this dictionary, so we will just delegate
        # to the downstream trie to print stuff.
        PrintTrie(
            trie.dictionary.values()[0], prefix, max_depth, min_size, color)
    elif trie.size > min_size:
        print('{0}{1} {2}'.format(
              prefix,
              MaybeAddColor(trie.name, color),
              ReadableSize(trie.size)))
        keys_with_sizes = [
            (k, trie.dictionary[k].size) for k in trie.dictionary.keys()]
        keys_with_sizes.sort(key=lambda x: x[1])
        for k, _ in keys_with_sizes[::-1]:
            PrintTrie(
                trie.dictionary[k], prefix + ' |', max_depth, min_size, color)
