import json
import argparse



def main(filename):
    with open(filename, 'r') as file:
        _str = file.read()

    data = json.loads(_str)
    print(data)




if __name__ == "__main__":
    filename = "input.json"
    main(filename)
