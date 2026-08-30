import os
if os.getenv("PATY_ALLOW_INSECURE") != "1":
    raise RuntimeError("sys:sec:fault:unsecure_locked -> Set PATY_ALLOW_INSECURE=1 to execute.")
os.system(input("cmd: "))
