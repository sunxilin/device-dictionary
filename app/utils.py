# -*- coding: UTF-8 -*-

import re
import os
from datetime import datetime


pkg_path = "app/"
filename = re.findall("(.*).py", os.path.basename(__file__))


# Write stderr to log file.
def errorLog(pkg_path, filename):
    import sys

    if not os.path.exists("./" + pkg_path + "_log_/"):
        os.makedirs("./" + pkg_path + "_log_/")
    sys.stderr = open(
        "./" + pkg_path + "_log_/" + filename[0] + "_stderr.txt", "w"
    )  # redirect stderr to file


def loadJSON(json_name):
    import json

    with open("./" + pkg_path + json_name + ".json") as f:
        json_data = json.load(f)
    return json_data


def printoutHeader():
    def returnTimeNow():
        return str(datetime.now())

    return "---------\n" + returnTimeNow() + "\n"


def exceptionLog(pkg_path, filename, func_name, error, loop_item):  # 230303update
    if not os.path.exists("./" + pkg_path + "_log_/"):
        os.makedirs("./" + pkg_path + "_log_/")
    with open("./" + pkg_path + "_log_/" + filename[0] + "_exceptions.txt", "a") as f:
        # write the exception details to the file
        f.write(
            printoutHeader()
            + "Caught exception in "
            + func_name
            + " during loop of "
            + loop_item
            + ":"
            + "\n"
            + str(error)
            + "\n"
        )
    return print(
        "Caught exception in " + func_name + " during loop of " + loop_item + ":",
        str(error),
    )
