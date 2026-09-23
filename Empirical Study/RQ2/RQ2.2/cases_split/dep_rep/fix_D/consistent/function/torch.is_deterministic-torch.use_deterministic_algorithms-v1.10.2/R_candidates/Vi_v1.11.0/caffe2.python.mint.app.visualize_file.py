def visualize_file(filename):
    fullname = os.path.join(args.root, filename)
    if filename.endswith('summary'):
        return visualize_summary(fullname)
    elif filename.endswith('log'):
        return visualize_print_log(fullname)
    else:
        return flask.jsonify(
            result='Unsupport file: {}'.format(filename),
            script=''
        )
