from git import Repo, exc
import sys
import json
import os
import argparse

def startProg():
    parser = argparse.ArgumentParser(description='gitHandshakes project')
    parser.add_argument('--input', type=str, help="Введите входной repo")
    parser.add_argument('--output', type=str, help='Введите name.json')
    args = parser.parse_args()
    path_to_data_json = f'{os.getcwd()}/data/{args.output}'
    if (args.input == None and args.output == None):
        print("Введите данные!")
        sys.exit()
    else: 
        if ((args.input == None) and (os.path.exists(path_to_data_json))):
            return [None , path_to_data_json]# true - json exists, start with the 2nd part of the program
        else: 
            if ((args.input == None) and os.path.exists(path_to_data_json) == False):
                print("Неккоректно введены данные --output")
                sys.exit()
            else:
                if ((args.input) and args.output == None):
                    parts = args.input.split("/")
                    last_word = parts[-1]
                    return [args.input ,f'{os.getcwd()}/data/{last_word}.json']
                else: 
                    return [args.input, f'{os.getcwd()}/data/{args.output}']

def collect_data(res_of_start):
    try:
        repo = Repo(res_of_start[0])
    except exc.InvalidGitRepositoryError:
        print(f"{res_of_start[0]} не является Git-репозиторием.")
        sys.exit()
    except exc.NoSuchPathError:
        print(f"Путь {res_of_start[0]} не существует.")
        sys.exit()
    # getting a list of recent commits
    try:
        commits = list(repo.iter_commits())
        print("Формируется набор данных для решения задачи, пожалуйста, ожидайте...")
    except ValueError:
        print(f"Ошибка git-репозитория")
        sys.exit()
    # creating dictionary - key: file, value: commiters 
    data_dict = creat_dict(commits)
    data_dict = filtering_source_with_one_programmer(data_dict) # deleting source with one programmer
    # print(data_dict)
    fileNameJson = res_of_start[1]
    saved_to_json(data_dict, fileNameJson)
    # return f'{fileNameJson}.json'

# creating dictionary - key: file, value: commiters  
def creat_dict(commits):
    data_dict = {}
    for commit in commits:
        if commit.parents:
            diff = commit.diff(commit.parents[0])  # comparison with the first parent
        else:
            diff = commit.diff(None)  # for the root commit
        # changes in all commit files
        for change in diff: 
            if change.a_path: # the path to the file before the change (if the file was deleted).
                if (f'{change.a_path}' not in data_dict):
                    data_dict[f'{change.a_path}'] = {commit.author.name + " " + commit.author.email}
                else:
                    data_dict[f'{change.a_path}'].add(commit.author.name + " " + commit.author.email)
            else: # the path to the file after the change (if the file was added or renamed).
                if (f'{change.b_path}' not in data_dict):
                    data_dict[f'{change.b_path}'] = {commit.author.name + " " + commit.author.email}
                else:
                    data_dict[f'{change.b_path}'].add(commit.author.name + " " + commit.author.email)
    return data_dict

# deleting files with one programmer
def filtering_source_with_one_programmer(data_dict):
    del_source = []
    for source in data_dict.keys():
        if (len(data_dict.get(source)) == 1):
            del_source.append(source)
        data_dict[source] = list(data_dict[source])
    for source in del_source:
        data_dict.pop(source)
    return data_dict

def saved_to_json(data_dict, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)
        return True
    return False