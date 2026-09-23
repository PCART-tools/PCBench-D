def main():
    parser = argparse.ArgumentParser(description='Tool to create a commit list')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--create_new', nargs=2)
    group.add_argument('--update_to')
    group.add_argument('--stat', action='store_true')
    group.add_argument('--export_markdown', action='store_true')

    parser.add_argument('--path', default='results/commitlist.csv')
    args = parser.parse_args()

    if args.create_new:
        create_new(args.path, args.create_new[0], args.create_new[1])
        return
    if args.update_to:
        update_existing(args.path, args.update_to)
        return
    if args.stat:
        commits = CommitList.from_existing(args.path)
        stats = commits.stat()
        pprint.pprint(stats)
        return
    if args.export_markdown:
        commits = CommitList.from_existing(args.path)
        categories = list(commits.stat().keys())
        for category in categories:
            print(f"Exporting {category}...")
            lines = get_markdown_header(category)
            lines += to_markdown(commits, category)
            filename = f'results/export/result_{category}.md'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                f.writelines(lines)
        return
    assert False
