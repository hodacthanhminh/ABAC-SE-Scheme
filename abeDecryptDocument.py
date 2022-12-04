# libs
import os
from os.path import join, dirname
import sys
import getopt
import json
# class/funcs
from abe.decryptDocument import DecryptDocument
from abe.utils import groupObj, loadObject, remove_unuse_key

from dotenv import load_dotenv

parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
GPP_IP = os.environ.get("GPP_IP")


def getArgv(argv):
    attribute_path = ""
    document_path = ""
    arg_help = "{0} -d <Encrypt Document Path> -a <User Attribute Path> ".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hd:a:", ["help", "document=", "attribute="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-a", "--attribute"):
            attribute_path = arg
        elif opt in ("-d", "--attribute"):
            document_path = arg
    return (document_path, attribute_path)


if __name__ == "__main__":
    (document_path, user_path) = getArgv(sys.argv)
    user_attribute = loadObject(user_path)
    # GPP = loadObject("GPP.txt")
    ddc = DecryptDocument(groupObj)
    with open(document_path, "r") as f:
        document = json.load(f)
    ddc.set_GPP(GPP_IP)
    print(ddc.get_result(document, user_attribute))
