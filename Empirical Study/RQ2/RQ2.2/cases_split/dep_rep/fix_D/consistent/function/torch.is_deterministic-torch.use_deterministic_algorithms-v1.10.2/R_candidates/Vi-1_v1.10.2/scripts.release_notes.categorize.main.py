def main():
    parser = argparse.ArgumentParser(description='Tool to help categorize commits')
    parser.add_argument('--category', type=str, default='Uncategorized',
                        help='Which category to filter by. "Uncategorized", None, or a category name')
    parser.add_argument('--file', help='The location of the commits CSV',
                        default='results/commitlist.csv')

    args = parser.parse_args()
    categorizer = Categorizer(args.file, args.category)
    categorizer.categorize()
