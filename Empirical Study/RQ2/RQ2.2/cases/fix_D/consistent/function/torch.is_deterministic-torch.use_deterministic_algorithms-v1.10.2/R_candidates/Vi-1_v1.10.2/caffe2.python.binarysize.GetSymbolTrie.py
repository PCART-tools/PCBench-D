def GetSymbolTrie(target, nm_command, max_depth):
    """Gets a symbol trie with the passed in target.

    Args:
            target: the target binary to inspect.
            nm_command: the command to run nm.
            max_depth: the maximum depth to create the trie.
    """
    # Run nm to get a dump on the strings.
    proc = subprocess.Popen(
        [nm_command, '--radix=d', '--size-sort', '--print-size', target],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    nm_out, _ = proc.communicate()
    if proc.returncode != 0:
        print('NM command failed. Output is as follows:')
        print(nm_out)
        sys.exit(1)
    # Run c++filt to get proper symbols.
    proc = subprocess.Popen(['c++filt'],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    out, _ = proc.communicate(input=nm_out)
    if proc.returncode != 0:
        print('c++filt failed. Output is as follows:')
        print(out)
        sys.exit(1)
    # Splits the output to size and function name.
    data = []
    for line in out.split('\n'):
        if line:
            content = line.split(' ')
            if len(content) < 4:
                # This is a line not representing symbol sizes. skip.
                continue
            data.append([int(content[1]), ' '.join(content[3:])])
    symbol_trie = Trie('')
    for size, name in data:
        curr = symbol_trie
        for c in name:
            if c not in curr.dictionary:
                curr.dictionary[c] = Trie(curr.name + c)
            curr = curr.dictionary[c]
            curr.size += size
            if len(curr.name) > max_depth:
                break
    symbol_trie.size = sum(t.size for t in symbol_trie.dictionary.values())
    return symbol_trie
