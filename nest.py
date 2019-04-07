import json
import argparse
import logging
import sys
import os
from tabulate import tabulate

# Creating an object
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Setting the threshold of logger to DEBUG
logger = logging.getLogger(__name__)


COLUMN_MAP = {}
FILE_HEADER = []        # stored keys from raw json file
SN_HEADER = []          # stores FILE_HEADER with extra key "S No."
master_json = {}        # final output json


def read_json_file(filename):
    """
    Reads a file containing JSON data
    :param filename: string
    :return: dict in json format
    """
    if not os.path.exists(filename):
        logger.error("File not Found!")
        sys.exit(1)
    if not os.path.isfile(filename):
        logger.error("Not a file! Please specify a valid filename with extension.")
        sys.exit(1)

    with open(filename, 'r') as file:
        logger.info("Reading file: '%s'", os.path.abspath(filename))
        _str = file.read()

    data = None
    try:
        data = json.loads(_str)
        # print(data)
    except ValueError as e:
        logger.error("Error parsing JSON file. Invalid JSON file: %s", filename, exc_info=True)
        sys.exit(1)

    return parse(data)


def parse(data):
    """
    Reads data in dict format and creates a table for representation
    :param data:
    :return:
    """
    global FILE_HEADER
    compute_headers(data)

    table = []
    # table.append(["S No.", "country", "city", "currency", "amount"])      # adding header as 1st row
    for i, item in enumerate(data):
        row = []
        row.append(i+1)
        for head in FILE_HEADER:
            row.append(item[head])
        # row.append(item['country'])
        # row.append(item['city'])
        # row.append(item['currency'])
        # row.append(item['amount'])
        table.append(row)

    logger.info("\n%s", tabulate(table, headers=SN_HEADER))
    # logger.info("\n%s", tabulate(table, headers=["S No.", "country", "city", "currency", "amount"]))
    # print(tabulate(table, headers=["S No.", "country", "city", "currency"]))

    logger.debug(table)
    return table


def compute_headers(data):
    global FILE_HEADER
    if isinstance(data, list):
        FILE_HEADER = list(data[0].keys())
        logger.debug("FILE_HEADER=%s", FILE_HEADER)
        update_sn_header()
        return FILE_HEADER
    else:
        logger.error("Error parsing JSON HEADERS. Invalid JSON file: %s", filename, exc_info=True)
        sys.exit(1)


def update_sn_header():
    global FILE_HEADER, SN_HEADER
    SN_HEADER = FILE_HEADER.copy()
    SN_HEADER.insert(0, "S No.")  # inject "S No."
    logger.debug("SN_HEADER=%s", SN_HEADER)


def column_mapper(out_header=None):
    global COLUMN_MAP
    # header = ["S No.", "country", "city", "currency", "amount"]
    logger.info("out_header=%s", out_header)
    if not out_header:
        logger.error("Unable to create COLUMN_MAP!")
        sys.exit(1)

    counter = 0
    for item in out_header:
        if item not in COLUMN_MAP.keys():
            COLUMN_MAP[item] = counter
            counter += 1
    logger.debug("COLUMN_MAP= %s", COLUMN_MAP)


def create_wireframe(level=1, *args):
    """
    creates a wire-frame json(dict) using the format of *args
    """

    frame = {}
    logger.debug("\nlevel=%s args=%s", level, args[0])
    if len(args[0]) < 1:
        logger.debug("returning...[amount k:v]")
        return ['amount k:v']

    # above leaf node still
    if len(args[0]) >= 1:
        for _argKey in args[0]:
            if not _argKey in frame.keys():
                d = create_wireframe(level + 1, tuple(_trimArgs(args)[1:]))
                frame[_argKey] = d
            break
    elif len(args[0]) == 1:
        logger.debug("leaf node reached, attach as a list")
        frame = []
        frame.append(args[0][0])


    logger.debug("returning...frame=%s", frame)
    return frame


def _trimArgs(arg):
    list_args = [x for x in arg[0]]
    return list_args


def data_preparer(frame, table_data):
    global master_json
    for row in table_data:
        d = filler(frame, row)
        logger.debug("\nd=%s", d)

        if len(master_json.keys()) == 0:
            master_json = d
        elif len(d.keys()) == 1:  #has to be one only
            master_json_cpy = master_json
            x = data_presser(d, master_json_cpy)
            # print("x=", x)
            master_json = x
        else:
            logger.error("ERROR!!!!!")
    logger.info("final master_json=%s", master_json)
    return master_json


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


def filler(reduced_frame, table_row):
    global COLUMN_MAP
    # print(">frame=", reduced_frame)
    # print(">row=", table_row)
    data = {}

    if isinstance(reduced_frame, dict):
        for key in reduced_frame.keys():        #there has to be only one key
            key_pos = COLUMN_MAP[key]
            key_data = table_row[key_pos]
            logger.debug("key=%s, key_pos=%s, data=%s", key, key_pos, key_data)
            _val = reduced_frame[key]           #new trimmed frame
            data[key_data] = filler(_val, table_row)

    elif isinstance(reduced_frame, list):   #last node leaf
        # print("......compute last node leaf")
        key_pos_ = COLUMN_MAP['amount']
        key_data_ = table_row[key_pos_]
        logger.debug("key='amount', key_pos=%s, data=%s", key_pos_, key_data_)
        leaf_data = []
        data['amount'] = key_data_
        leaf_data.append(data)
        return leaf_data

    return data


def main(args):
    logger.info("Starting...")

    # Read JSON file
    filename = args.filename  # input from cmd line
    table_data = read_json_file(filename)
    print("table_data=", table_data)

    # nesting_level_list = ["country", "city", "country", "currency"]     #input from cmd line
    nesting_level_list = args.nesting_level_1
    # s_no = ["S No."]
    # s_no.extend(nesting_level_list)
    nesting_level_list.insert(0, "S No.")
    # add "amount" as mandatory leaf dict
    if "amount" not in nesting_level_list:
        nesting_level_list.extend(["amount"])

    logger.debug("FINAL nesting_level_list=%s", nesting_level_list)
    column_mapper(SN_HEADER)

    frame = create_wireframe(1, nesting_level_list[1:])  # don't send "S No." for creting wireframe
    # frame = magic(1, ["currency", "country", "city"])
    logger.info(">final frame = %s", frame)

    logger.info("Now filling data into frame...")
    output = data_preparer(frame, table_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This is nested dictionary challenge program.")
    parser.add_argument("filename", help="filename containing a valid json", type=str)
    parser.add_argument("nesting_level_1", help="Specify atleast one nesting level", type=str, nargs='+')
    parser.add_argument("-v", "--verbose", help="increase verbosity", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.info("-verbosity turned on")

    logger.info(args.nesting_level_1)

    main(args)

    # logger.info("Starting...")
    #
    # # Read JSON file
    # filename = args.filename        #input from cmd line
    # table_data = read_json_file(filename)
    # print("table_data=", table_data)
    #
    # # nesting_level_list = ["country", "city", "country", "currency"]     #input from cmd line
    # nesting_level_list = args.nesting_level_1
    # # s_no = ["S No."]
    # # s_no.extend(nesting_level_list)
    # nesting_level_list.insert(0, "S No.")
    # # add "amount" as mandatory leaf dict
    # if "amount" not in nesting_level_list:
    #     nesting_level_list.extend(["amount"])
    #
    # logger.debug("FINAL nesting_level_list=%s", nesting_level_list)
    # column_mapper(SN_HEADER)
    #
    # frame = create_wireframe(1, nesting_level_list[1:])     # don't send "S No." for creting wireframe
    # # frame = magic(1, ["currency", "country", "city"])
    # logger.info(">final frame = %s", frame)
    #
    # logger.info("Now filling data into frame...")
    # output = data_preparer(frame, table_data)
