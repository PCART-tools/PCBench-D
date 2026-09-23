def gen_serialized_test_coverage(source_dir, output_dir):
    (covered, not_covered, schemaless) = gen_coverage_sets(source_dir)
    num_covered = len(covered)
    num_not_covered = len(not_covered)
    num_schemaless = len(schemaless)
    total_ops = num_covered + num_not_covered

    with open(os.path.join(output_dir, 'SerializedTestCoverage.md'), 'w+') as f:
        f.write('# Serialized Test Coverage Report\n')
        f.write("This is an automatically generated file. Please see "
            "`caffe2/python/serialized_test/README.md` for details. "
            "In the case of merge conflicts, please rebase and regenerate.\n")
        f.write('## Summary\n')
        f.write(
            'Serialized tests have covered {}/{} ({}%) operators\n\n'.format(
                num_covered, total_ops,
                (int)(num_covered / total_ops * 1000) / 10))

        f.write('## Not covered operators\n')
        f.write('<details>\n')
        f.write(
            '<summary>There are {} not covered operators</summary>\n\n'.format(
                num_not_covered))
        for n in sorted(not_covered):
            f.write('* ' + n + '\n')
        f.write('</details>\n\n')

        f.write('## Covered operators\n')
        f.write('<details>\n')
        f.write(
            '<summary>There are {} covered operators</summary>\n\n'.format(
                num_covered))
        for n in sorted(covered):
            f.write('* ' + n + '\n')
        f.write('</details>\n\n')

        f.write('## Excluded from coverage statistics\n')
        f.write('### Schemaless operators\n')
        f.write('<details>\n')
        f.write(
            '<summary>There are {} schemaless operators</summary>\n\n'.format(
                num_schemaless))
        for n in sorted(schemaless):
            f.write('* ' + n + '\n')
        f.write('</details>\n\n')
