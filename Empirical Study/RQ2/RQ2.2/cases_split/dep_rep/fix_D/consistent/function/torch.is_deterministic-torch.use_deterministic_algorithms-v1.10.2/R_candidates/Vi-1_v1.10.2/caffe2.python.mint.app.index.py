@app.route('/')
def index():
    files = glob.glob(os.path.join(args.root, "*.*"))
    files.sort()
    names = [os.path.basename(f) for f in files]
    return flask.render_template(
        'index.html',
        root=args.root,
        names=names,
        debug_messages=names
    )
