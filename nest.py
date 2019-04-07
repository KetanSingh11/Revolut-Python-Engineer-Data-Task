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
        print("returning...[amount]")
        return ['amount k:v']

    #above leaf node still
    if len(args[0]) >= 1:
        for _argKey in args[0]:
            if not _argKey in frame.keys():
                d = magic(level + 1, tuple(_trimArgs(args)[1:]))
                frame[_argKey] = d
            break
    elif len(args[0]) == 1:
        print("leaf node reached, attach as a list")
        # frame[args[0][0]] = []
        frame = []
        frame.append(args[0][0])

    # list_args = [x for x in args[0]]
    # magic("bb", tuple(list_args[1:]))

    print("returning...frame=", frame)
    return frame


def _trimArgs(arg):
    list_args = [x for x in arg[0]]
    return list_args

master_json = {}

def data_preparer(frame, table_data):
    global master_json
    for row in table_data:
        d = filler(frame, row)
        print("\nd=", d, "\n")

        if len(master_json.keys()) == 0:
            master_json = d
        elif len(d.keys()) == 1:  #has to be one only
            master_json_cpy = master_json
            x = data_presser(d, master_json_cpy)
            print("x=", x)
            master_json = x
        else:
            print("ERROR!!!!!")
    print("final master_json=", master_json)

def data_presser(d, master_json_cpy):
    # global master_json      #filled up

    if isinstance(d, dict):
        d_key = list(d.keys())[0]
        if d_key in master_json_cpy.keys():     #key is same
            d_cpy = d[d_key]
            # master_json_cpy_ = master_json_cpy[list(master_json_cpy.keys())[d_key]]
            master_json_cpy_ = master_json_cpy[d_key]
            master_json_cpy[d_key] = data_presser(d_cpy, master_json_cpy_)

        else:                                   #key is different, add
            new_d = {}
            new_d.update(d)
            new_d.update(master_json_cpy)
            return new_d
    elif isinstance(d, list):
        return master_json_cpy.append(d)

    return master_json_cpy


    # if list(d.keys())[0] in master_json.keys():
    #     print("pressed master_data=")
    #     master_json[list(d.keys())[0]][list(d.keys())[0]] = d[list(d.keys())[0]][list(d.keys())[0]]
    #     print(master_json)
    # else:
    #     print("--new key in new row")
    #     d_only_key = list(d.keys())[0]
    #     master_json[d_only_key] = d[d_only_key]


def filler(reduced_frame, table_row):
    global COLUMN_MAP
    # print(">frame=", reduced_frame)
    # print(">row=", table_row)
    data = {}

    if isinstance(reduced_frame, dict):
        for key in reduced_frame.keys():        #there has to be only one key
            key_pos = COLUMN_MAP[key]
            key_data = table_row[key_pos]
            # print("key=", key, " key_pos=", key_pos, "data=", key_data)
            _val = reduced_frame[key]           #new trimmed frame
            data[key_data] = filler(_val, table_row)

    elif isinstance(reduced_frame, list):   #last node leaf
        # print("......compute last node leaf")
        key_pos_ = COLUMN_MAP['amount']
        key_data_ = table_row[key_pos_]
        # print("key=", 'amount', " key_pos=", key_pos_, "data=", key_data_)
        leaf_data = []
        data['amount'] = key_data_
        leaf_data.append(data)
        return leaf_data

    return data




if __name__ == "__main__":
    filename = "input.json"
    table_data = main(filename)
    # print(table_data)
    column_mapper()

    # frame = magic(1, ["country", "city", "country", "currency"])
    frame = magic(1, ["currency", "country", "city"])
    print("> final frame = ", frame)

    print("\n>inside filler...")
    data_preparer(frame, table_data)