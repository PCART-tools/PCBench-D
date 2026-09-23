def error_msg_wx(msg, parent=None):
    """Signal an error condition with a popup error dialog."""
    dialog = wx.MessageDialog(parent=parent,
                              message=msg,
                              caption='Matplotlib backend_wx error',
                              style=wx.OK | wx.CENTRE)
    dialog.ShowModal()
    dialog.Destroy()
    return None
