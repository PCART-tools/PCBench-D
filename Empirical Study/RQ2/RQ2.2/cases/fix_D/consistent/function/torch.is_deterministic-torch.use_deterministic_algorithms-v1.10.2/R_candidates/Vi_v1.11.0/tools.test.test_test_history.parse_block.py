def parse_block(block: List[str]) -> Optional[Example]:
    if block:
        match = re.match(r'^\$ ([^ ]+) (.*)$', block[0])
        if match:
            cmd, first = match.groups()
            args = []
            for i, line in enumerate([first] + block[1:]):
                if line.endswith('\\'):
                    args.append(line[:-1])
                else:
                    args.append(line)
                    break
            return {
                'cmd': cmd,
                'args': shlex.split(''.join(args)),
                'lines': block[i + 1:]
            }
    return None
