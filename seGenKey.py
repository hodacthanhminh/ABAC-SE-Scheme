# libs
import sys
import getopt
# pse
from se.genkey import GenKey
from se.contants import d, L


def myfunc(argv):
    key_path = ""
    key_id = ""
    arg_help = "{0} -p <Key Path> -i <Key ID> ".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hp:i:", ["help", "path=",
                                                       "id="])
    except:
        print(arg_help)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-p", "--path"):
            key_path = arg
        elif opt in ("-i", "--id"):
            key_id = arg
    return (key_path, key_id)

if __name__ == "__main__":
    key = GenKey(d, L)
    (key_path, key_id) = myfunc(sys.argv)
    key.write_key(key_path, key_id)
