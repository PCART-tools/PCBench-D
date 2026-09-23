@pytest.mark.parametrize('kwargs', generate_errorbar_inputs())
def test_errorbar_inputs_shotgun(kwargs):
    ax = plt.gca()
    eb = ax.errorbar(**kwargs)
    eb.remove()
