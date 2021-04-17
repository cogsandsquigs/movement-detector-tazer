from random import *

for i in range(1000):
    with open(str(i) + "owo" + str(random()) + ".vb", "w") as f:
        f.write("""Create a new text file!""")
