from libs.func import collect_data
from libs.graph import gr, max_handshakes


repo_path = str(input("Введите путь к репозиторию: "))
# collect the data set
data_dict = collect_data(repo_path)
# creating a programmer graph
G = gr(data_dict)
# max lenth of handshakers between programmers
max_handshakes(G)