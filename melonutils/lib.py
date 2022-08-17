import pandas as pd # type: ignore
from os.path import abspath
from os.path import dirname

def get_core():
    """
    Create core
    """
    return "a lot of core"

def clean_core(core):
    """
    Clean core
    """
    return core.upper()

def make_result(df, filename):
    """
    Write output result in filename
    """
    df.drop(["datetime", "timestamp", "score_value"], axis=1, inplace=True)
    df["player"] = df.player.str.upper()
    df.to_csv(filename)
    print(" {} Made")
    
if __name__ == "__main__":
    import melonutils
    
    datapath = dirname(abspath(melonutils.__file__)) + "/core"
    core = "{}/core.csv".format(datapath)
    df = pd.read_csv(core)
    core = get_core()
    clean_core = clean_core(core)
    print("df, core and clean_core made.")
    