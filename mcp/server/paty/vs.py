#!/usr/init/env python3
import sys
import os

def entry_point():
    base_dir = os.path.expanduser("~/Paty-vulgarsota-")
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
    os.chdir(base_dir)
    
    from main import main as run_main
    run_main()

if __name__ == "__main__":
    entry_point()
