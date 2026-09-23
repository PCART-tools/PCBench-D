def parse_description(description: str) -> List[Example]:
    examples: List[Example] = []
    for block in description.split('\n\n'):
        matches = [
            re.match(r'^    (.*)$', line)
            for line in block.splitlines()
        ]
        if all(matches):
            lines = []
            for match in matches:
                assert match
                line, = match.groups()
                lines.append(line)
            example = parse_block(lines)
            if example:
                examples.append(example)
    return examples
