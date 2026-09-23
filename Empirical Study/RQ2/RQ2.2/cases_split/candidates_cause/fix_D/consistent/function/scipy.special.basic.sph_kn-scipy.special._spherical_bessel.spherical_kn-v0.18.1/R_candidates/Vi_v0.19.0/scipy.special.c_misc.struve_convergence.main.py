def main():
    plt.clf()
    plt.subplot(121)
    do_plot(True)
    plt.title('Struve H')

    plt.subplot(122)
    do_plot(False)
    plt.title('Struve L')

    plt.savefig('struve_convergence.png')
    plt.show()
