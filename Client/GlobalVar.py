# ---------------------------------------
# Function: Global Variables Setting
# Coding: utf-8
# ---------------------------------------


# Initialization
def _init():
    global _global_dict
    _global_dict = {}

# Set global variable value
def setVal(key, value):
    _global_dict[key] = value

# Fetch global variable value
def getVal(key):
    try:
        return _global_dict[key]
    except Exception:
        print("Read"+key+"fails\r\n")