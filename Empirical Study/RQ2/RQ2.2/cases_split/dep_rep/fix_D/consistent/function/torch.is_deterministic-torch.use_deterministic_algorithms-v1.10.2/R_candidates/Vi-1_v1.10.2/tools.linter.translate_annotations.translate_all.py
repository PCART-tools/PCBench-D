def translate_all(
    *,
    lines: List[str],
    regex: Pattern[str],
    commit: str
) -> List[Annotation]:
    ann_dict: DefaultDict[str, List[Annotation]] = defaultdict(list)
    for line in lines:
        annotation = parse_annotation(regex, line)
        if annotation is not None:
            ann_dict[annotation['filename']].append(annotation)
    ann_list = []
    for filename, annotations in ann_dict.items():
        raw_diff = subprocess.check_output(
            ['git', 'diff-index', '--unified=0', commit, filename],
            encoding='utf-8',
        )
        diff = parse_diff(raw_diff) if raw_diff.strip() else None
        # if there is a diff but it doesn't list an old filename, that
        # means the file is absent in the commit we're targeting, so we
        # skip it
        if not (diff and not diff['old_filename']):
            for annotation in annotations:
                line_number: Optional[int] = annotation['lineNumber']
                if diff:
                    annotation['filename'] = cast(str, diff['old_filename'])
                    line_number = translate(diff, cast(int, line_number))
                if line_number:
                    annotation['lineNumber'] = line_number
                    ann_list.append(annotation)
    return ann_list
