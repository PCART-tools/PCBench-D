def new_date(d):
    "Generate a safe date from a datetime.date object."
    return date(d.year, d.month, d.day)
