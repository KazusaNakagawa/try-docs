import sys
import pdb


class Arg(object):

    def __init__(self, env=sys.argv[2]):
        self.env = env


if __name__ == '__main__':
    arg = Arg()
    print(arg.env)
