@image_comparison(['figure_suptitle'])
def test_suptitle():
    fig, _ = plt.subplots()
    fig.suptitle('hello', color='r')
    fig.suptitle('title', color='g', rotation='30')
