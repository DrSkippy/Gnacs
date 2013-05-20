#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import gnacs

def main():
    args = sys.argv[1:]
    sys.argv = [gnacs.__file__] + args + ["-z", "tumblr"]
    gnacs.main()

if __name__ == "__main__":
    main()
