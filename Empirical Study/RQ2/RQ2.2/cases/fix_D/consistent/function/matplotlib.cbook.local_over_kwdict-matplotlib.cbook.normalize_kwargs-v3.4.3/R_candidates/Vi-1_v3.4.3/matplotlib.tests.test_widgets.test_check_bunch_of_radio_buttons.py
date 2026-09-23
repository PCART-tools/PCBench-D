@image_comparison(['check_bunch_of_radio_buttons.png'],
                  style='mpl20', remove_text=True)
def test_check_bunch_of_radio_buttons():
    rax = plt.axes([0.05, 0.1, 0.15, 0.7])
    widgets.RadioButtons(rax, ('B1', 'B2', 'B3', 'B4', 'B5', 'B6',
                               'B7', 'B8', 'B9', 'B10', 'B11', 'B12',
                               'B13', 'B14', 'B15'))
