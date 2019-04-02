import json
import argparse
from tabulate import tabulate


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
        # row.append(item['country'])
        # row.append(item['city'])
        row.append(item['currency'])
        row.append(item['amount'])
        table.append(row)


    # print(tabulate(table, headers=["S No.", "country", "city", "currency", "amount"]))
    # print(tabulate(table, headers=["S No.", "currency", "amount"]))

    print(table)
    return table

def column_mapper():
    pass

def magic(level=1, *args):
    frame = {}
    print("\nargs= ", args[0])
    if len(args[0]) < 1:
        print("returning...nothing")
        return

    #above leaf node still
    if len(args[0]) > 1:
        for _t in args[0]:
            if not _t in frame.keys():
                frame[_t] = {}
    elif len(args[0]) == 1:
        # leaf node reached, attach list
        frame[args[0][0]] = []

    print("frame=", frame)
    list_args = [x for x in args[0]]
    magic("bb", tuple(list_args[1:]))

    print("returning...", frame)
    return frame


def filler(frame, table_data):
    data = {}
    for key, val in frame.items():
        pass




if __name__ == "__main__":
    filename = "input.json"
    table_data = main(filename)
    # print(table)

    frame = magic("sf", ["city", "currency"])
    print(frame)

    filler(frame, table_data)