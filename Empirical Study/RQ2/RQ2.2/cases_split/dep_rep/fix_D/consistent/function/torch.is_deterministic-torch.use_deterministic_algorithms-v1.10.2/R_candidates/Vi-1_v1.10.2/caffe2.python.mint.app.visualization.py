@app.route('/visualization/<string:name>')
def visualization(name):
    ret = visualize_file(name)
    return ret
