def get_duplicates(values):
    """Return duplicate values in an iterable.

    :param values: Values to iterate over.
    :type: values: iterable
    :return: Duplicate values in an iterable.
    :rtype: list
    """
    uniques = set()
    duplicates = []

    for value in values:
        if value in uniques:
            duplicates.append(value)
        else:
            uniques.add(value)

    return duplicates
