def restart_with_reloader():
    new_environ = {**os.environ, DJANGO_AUTORELOAD_ENV: 'true'}
    args = get_child_arguments()
    while True:
        p = subprocess.run(args, env=new_environ, close_fds=False)
        if p.returncode != 3:
            return p.returncode
