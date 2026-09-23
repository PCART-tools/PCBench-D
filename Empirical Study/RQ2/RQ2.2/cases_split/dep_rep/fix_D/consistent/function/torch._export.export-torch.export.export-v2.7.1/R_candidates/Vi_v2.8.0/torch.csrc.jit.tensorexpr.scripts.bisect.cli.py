    @click.command()
    @click.option("--cmd", required=True)
    def cli(cmd):
        bisect(cmd)
