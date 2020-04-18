def convert_comma_separated(num):
    num_list = list(str(num))[::-1]
    if len(num_list) >= 10:
        num_list.insert(3, ",")
        num_list.insert(6, ",")
        num_list.insert(9, ",")
        num_list.insert(12, ",")
        new_num = "".join(num_list[::-1])
    elif len(num_list) >= 8:
        num_list.insert(3, ",")
        num_list.insert(6, ",")
        num_list.insert(9, ",")
        new_num = "".join(num_list[::-1])

    elif len(num_list) >= 6:
        num_list.insert(3, ",")
        num_list.insert(6, ",")
        new_num = "".join(num_list[::-1])
    elif len(num_list) > 3:
        num_list.insert(3, ",")
        new_num = "".join(num_list[::-1])
    else:
        new_num = "".join(num_list[::-1])
    return new_num
