def main(args):
    test_source([
        _REF_ENV_TEMPLATE.format(pr=args.pr),
        _PR_ENV_TEMPLATE.format(pr=args.pr),
    ])
    _main(args)
