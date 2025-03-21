import networkx as nx

# creating a programmer graph
def gr(data_dict):
    sources = list(data_dict.keys())
    # getting a set of programmers
    commiters = set()
    commiters = set(data_dict.get(sources[0]))
    for list_of_programmer in data_dict.keys():
        commiters = commiters.union(set(data_dict.get(list_of_programmer)))
    # creating a graph object
    G = nx.Graph() 
    handshake = [] # edges
    for source in sources: # creating pairs of programmers
        tmp_list_of_programmer = list(data_dict.get(source))
        for i in range(len(tmp_list_of_programmer) - 1):
            for j in range(i + 1, len(tmp_list_of_programmer)):
                handshake.append((tmp_list_of_programmer[i], tmp_list_of_programmer[j]))

    G.add_nodes_from(commiters)
    G.add_edges_from(handshake)
    return G

def max_handshakes(G):
    # creating a dictionary key- source, value - dictionary(key - target, value - length)
    dict_of_pair_lengths = dict(nx.all_pairs_shortest_path_length(G))
    max = 0
    for _, targets in dict_of_pair_lengths.items():
        for _, length in targets.items():
            if length > max: max = length
    print('Максимальное число "рукопожатий" между двумя программистами данного проекта: ', max)


# an additional unused feature of finding the shortest path between 2 programmers
def count_the_number_of_handshakes(G):
    print("Введите имена двух программистов через ENTER: ")
    source = input()
    target = input()
    if ((source not in G.nodes()) or (target not in G.nodes())):
        if (source not in G.nodes()): print(f'Программиста {source} нет в списке программистов проекта')
        if (target not in G.nodes()): print(f'Программиста {target} нет в списке программистов проекта')
    elif (nx.has_path(G, source, target)):
        path = nx.shortest_path(G, source, target, weight=None)
        result_path = " <-> ".join(path)
        print(f'Путь от {source} до {target}: {result_path}')
        print(f'Количество "рукопожатий" между программистами: {len(path) - 1}')
    else:
        print(f'Программисты {source} и {target} не "знакомы" в данном проекте')