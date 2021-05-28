import os
from typing import Tuple, Union
from github import Github
import sys

import github

# parse args
if len(sys.argv) != 2:
    print("Usage: dowload.py csv-file")
    sys.exit(1)

# my token on GitHub
with open("access_token.txt", "r") as token:
    g = Github(token.readline())


def get_file(repo_name_with_owner: str, path_to_file: str) -> Union[str, github.GithubException]:
    """Returns the content of the file on Github

    Args:
        repo_name_with_owner (str): Repo of the file, must include the owner
        path_to_file (str): Path from root of the repo to the file

    Returns:
        str: Decoded string representation of the file, works for text files only
    """
    # find repo, which may not exist
    try:
        repo = g.get_repo(repo_name_with_owner)
    except github.GithubException as e:
        print(f"Github API {e.status} response for non-existent repo: {repo_name_with_owner}", file=sys.stderr)
        return e

    # grab file
    try:
        contents = repo.get_contents(path_to_file)
    except github.GithubException as e:
        print(f"Github API {e.status} response for {repo_name_with_owner}/{path_to_file}", file=sys.stderr)
        return e

    return contents.decoded_content.decode('UTF-8')


def parse_url(url: str) -> Tuple[str, str]:
    """Parses the url into repo and file path

    Args:
        url (str): Full url to a file on Github

    Returns:
        Tuple[str, str]: Pair of the repo's name with owner and the path to file
    """
    url_split = url.split('/')
    repo, path = '/'.join(url_split[3:5]), '/'.join(url_split[7:]) 
    return repo, path


# open the csv with the indices
import csv
skip_first_line = True
with open(sys.argv[1], 'r') as data:
    for row in csv.reader(data):
        if skip_first_line:
            skip_first_line = False
            continue
        if len(row) != 2:
            print(f"Corrupted row in csv: {row}")
            continue
        
        repo_name, url = row

        # trim repo name, removing the /
        repo_name = repo_name[:-1]

        # parse url
        # ex:
        # https://www.github.com/0532/netty-demo/tree/master/nettysource/src/main/java/Channel.uml
        # becomes src/main/java/Channel.uml
        parsed_repo, parsed_file_path = parse_url(url)

        # data integrity check
        try:
            assert repo_name == parsed_repo
        except:
            print(f"Data integrity violated: {repo_name} vs {parsed_repo}", file=sys.stderr)
            continue

        # only get the files ending in .xmi
        if not parsed_file_path.endswith(".xmi"):
            continue

        content = get_file(repo_name, parsed_file_path)

        if isinstance(content,github.GithubException):
            pass
        else:
            # change the file path to a name of a file in the current folder
            tokens = parsed_file_path.split('/')
            downloaded = "--".join(tokens)
            
            with open(downloaded, 'w', encoding='UTF-8') as storage:
                storage.write(content)

