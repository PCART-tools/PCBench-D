def test_load_from_url():
    path = Path(__file__).parent / "baseline_images/pngsuite/basn3p04.png"
    url = ('file:'
           + ('///' if sys.platform == 'win32' else '')
           + path.resolve().as_posix())
    with _api.suppress_matplotlib_deprecation_warning():
        plt.imread(url)
    with urllib.request.urlopen(url) as file:
        plt.imread(file)
