@pytest.mark.backend('TkAgg', skip_on_importerror=True)
@_isolated_tk_test(success_count=1)
def test_figuremanager_preserves_host_mainloop():  # pragma: no cover
    import tkinter
    import matplotlib.pyplot as plt
    success = []

    def do_plot():
        plt.figure()
        plt.plot([1, 2], [3, 5])
        plt.close()
        root.after(0, legitimate_quit)

    def legitimate_quit():
        root.quit()
        success.append(True)

    root = tkinter.Tk()
    root.after(0, do_plot)
    root.mainloop()

    if success:
        print("success")
