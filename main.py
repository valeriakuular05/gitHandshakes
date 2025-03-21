from libs.func import collect_data, startProg
from libs.graph import gr, max_handshakes
import json


res_of_start = startProg() # [--input, --output]
if (res_of_start[0]):  #if --input repo --output name.json
    # collect the data set
    collect_data(res_of_start)

# start the 2nd part of the program 
with open(res_of_start[1], "r", encoding="utf-8") as file:
    data_dict = json.load(file)
G = gr(data_dict)
# max lenth of handshakers between programmers
max_handshakes(G)