from bbfreeze import Freezer
f = Freezer("jerboa_bin", includes=("parser","logger","upload","config"))
f.addScript("jerboa.py")
f()
