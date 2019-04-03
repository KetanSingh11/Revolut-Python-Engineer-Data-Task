import json
import argparse
from tabulate import tabulate

COLUMN_MAP = {}


def main(filename):
    with open(filename, 'r') as file:
        _str = file.read()

    data = json.loads(_str)
    # print(data)
    return parse(data)

def parse(data):
    table = []
    # table.append(["S No.", "country", "city", "currency", "amount"])
    for i, item in enumerate(data):
        row = []
        row.append(i+1)
        row.append(item['country'])
        row.append(item['city'])
        row.append(item['currency'])
        row.append(item['amount'])
        table.append(row)


    print(tabulate(table, headers=["S No.", "country", "city", "currency", "amount"]))
    # print(tabulate(table, headers=["S No.", "country", "city", "currency"]))

    print(table)
    return table

def column_mapper(header=["S No.", "country", "city", "currency", "amount"]):
    global COLUMN_MAP
    for i, item in enumerate(header):
        COLUMN_MAP[item] = i
    print("COLUMN_MAP=", COLUMN_MAP)


def magic(level=1, *args):
    """creates a wire-frame"""
    frame = {}
    print("\nlevel=", level, "  args= ", args[0])
    if len(args[0]) < 1:
        print("returning...nothing")
        return

    #above leaf node still
    if len(args[0]) > 1:
        for _t in args[0]:
            if not _t in frame.keys():
                d = magic(level+1, tuple(_tt(args)[1:]))
                frame[_t] = d
            break
    elif len(args[0]) == 1:
        print("leaf node reached, attach as a list")
        # frame[args[0][0]] = []
        frame = []
        frame.append(args[0][0])

    print("frame=", frame)
    # list_args = [x for x in args[0]]
    # magic("bb", tuple(list_args[1:]))

    print("returning...", frame)
    return frame


def _tt(arg):
    list_args = [x for x in arg[0]]
    return list_args


def filler(frame, table_data):
    global COLUMN_MAP
    print(">frame=", frame)
    data = {}
    l_data = []

    row_counter = 0
    while row_counter < len(table_data):
        print("row_counter=", row_counter)
        if isinstance(frame, dict):
            for key in frame.keys():        #theres only one key
                key_pos = COLUMN_MAP[key]
                key_data = table_data[row_counter][key_pos]
                print("key=", key, " key_pos=", key_pos, "data=", key_data)
                _val = frame[key]     #new trimmed frame
                if isinstance(_val, dict):
                    data[key_data] = filler(_val, table_data)   #filling empty dict
                    print("unreach")
                    break
                elif isinstance(_val, list):
                    data[key_data] = filler(_val, table_data)  # filling empty dict
                    # key_pos_ = COLUMN_MAP[_val[0]]
                    # key_data_ = table_data[row_counter][key_pos_]
                    # print("key=", _val[0], " key_pos=", key_pos_, "data=", key_data_)
                    # data = []
                    # data.append(key_data_)
                    # return data

        elif isinstance(frame, list):   #last node leaf
            print("......compute last node leaf")
            _val = frame[0]
            key_pos_ = COLUMN_MAP[_val]
            key_data_ = table_data[row_counter][key_pos_]
            print("key=", _val, " key_pos=", key_pos_, "data=", key_data_)
            l_data.append(key_data_)
            # return data

        row_counter += 1

    if l_data:
        print("\n", l_data)
        return l_data
    print("\n", data)
    return data





if __name__ == "__main__":
    filename = "input_2.json"
    table_data = main(filename)
    # print(table_data)
    column_mapper()

    # frame = magic(1, ["country", "city", "country", "currency"])
    frame = magic(1, ["city", "country"])
    print("> final frame = ", frame)

    print("\n>inside filler...")
    filler(frame, table_data)