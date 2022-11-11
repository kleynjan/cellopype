def deep_eq(left, right):
    # both sides must be of the same type
    if type(left) != type(right):
        return False

    # pandas types
    if "pandas" in str(type(left)):
        return left.equals(right)

    # convert left and right to dicts if possible, skip if they can't be converted
    try:
        left = left.__dict__
        right = right.__dict__
    except Exception:
        pass

    # compare the two objects or dicts key by key
    if type(left) == dict:
        for key in left:
            # check if the key is present in the right dict, if not, we are not equals
            if key not in right:
                return False
            else:
                # compare the values if the key is present in both sides
                if not deep_eq(left[key], right[key]):
                    return False

        # check if any keys are present in right, but not in left
        for key in right:
            if key not in left:
                return False

        return True

    # check for each item in lists
    if type(left) == list:
        # right and left must have the same length
        if len(left) != len(right):
            return False

        # compare each item in the list
        for index in range(len(left)):
            if not deep_eq(left[index], right[index]):
                return False

    # do a standard comparison
    return left == right
