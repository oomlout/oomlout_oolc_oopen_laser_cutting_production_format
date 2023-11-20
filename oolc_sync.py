import yaml
import oom_git
import copy

def main(**kwargs):
    repos = kwargs["repos"]
    repo_directory = "tmp/data"
    p3 = copy.deepcopy(kwargs)
    p3["directory"] = repo_directory
    for repo in repos:
        p4 = copy.deepcopy(p3)
        p4["repo"] = repo
        oom_git.clone(**p4)
        





if __name__ == "__main__":
    kwargs = {}
    repos = []
    with open("oolc_repos.yaml", 'r') as stream:
        try:
            repos = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)
    kwargs["repos"] = repos
    main(**kwargs)