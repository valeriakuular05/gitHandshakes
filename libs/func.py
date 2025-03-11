from git import Repo, exc
import sys


def collect_data(path):
    try:
        repo = Repo(path)
    except exc.InvalidGitRepositoryError:
        print(f"{path} не является Git-репозиторием.")
        sys.exit()
    except exc.NoSuchPathError:
        print(f"Путь {path} не существует.")
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
    data_dict = filtering_source_with_one_programmer(data_dict) # deleting files with one user
    return data_dict

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
                    data_dict[f'{change.a_path}'] = {commit.author.name}
                else:
                    data_dict[f'{change.a_path}'].add(commit.author.name)
            else: # the path to the file after the change (if the file was added or renamed).
                if (f'{change.b_path}' not in data_dict):
                    data_dict[f'{change.b_path}'] = {commit.author.name}
                else:
                    data_dict[f'{change.b_path}'].add(commit.author.name)
    return data_dict

# deleting files with one programmer
def filtering_source_with_one_programmer(data_dict):
    del_source = []
    for source in data_dict.keys():
        if (len(data_dict.get(source)) == 1):
            del_source.append(source)
    for source in del_source:
        data_dict.pop(source)
    return data_dict