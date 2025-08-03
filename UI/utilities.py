"""Functions that are used in more than one class"""

def prepare_dropdown_options_lists(list_of_options_lists):
    """
    Inserts an empty string at the beginning of each of the lists, to use as the default (unfiltered) value for a dropdown menu.
    Also orders the list alphabetically. Does these actions in-place (i.e. modifies existing lists)
    """
    for options in list_of_options_lists:
        options.sort(key=str.lower) # alphabetise list

        options.insert(0, "") # add empty string at start
