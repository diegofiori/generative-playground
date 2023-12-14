from dataclasses import dataclass
import os
from typing import Any, Dict, List

from github import Github, GithubException


@dataclass
class GitHubInterface:
    """Wrapper for GitHub API."""

    github: Github
    github_repository: str
    github_branch: str | None = None
    github_base_branch: str | None = None
    
    def get_status(self) -> str:
        """
        Gets the status of the GitHub interface. 
        This method is not for the model to be used but its for giving the assistant 
        the context at the start of the conversation.
        Returns:
            str: The status of the GitHub interface
        """
        try:
            commits = list(self.github_repo_instance.get_commits())
        except Exception as e:
            print(e)
            commits = []
        
        if len(commits) > 10:
            commits = commits[-10:]
        
        return {
            "github_repository": self.github_repository,
            "github_branch": self.github_branch,
            "github_base_branch": self.github_base_branch,
            "files": self.get_files(),
            "commit_history": commits,
        }
        
    def get_files(self, path=""):
        """
        Gets all the files in the repository, including those in subdirectories.
        Returns:
            List[str]: The files in the repository
        """
        files = []
        try:
            contents = self.github_repo_instance.get_contents(path)
        except Exception as e:
            print(e)
            contents = []

        for content in contents:
            if content.type == "dir":
                files.extend(self.get_files(content.path))
            else:
                files.append(content.path)

        return files
    
    @classmethod
    def from_github_token(cls, github_token: str, repository: str, **kwargs) -> "GitHubInterface":
        """
        Creates a GitHubInterface from a GitHub token
        Parameters:
            github_token(str): The GitHub token
        Returns:
            GitHubInterface: The GitHubInterface object
        """
        github = Github(github_token)
        return cls(github=github, github_repository=repository, **kwargs)
    
    def __post_init__(self):
        self.github_repo_instance = self.github.get_repo(self.github_repository)
        # default value for branch is main
        if self.github_branch is None:
            self.github_branch = "main"
        # default value for base branch is main
        if self.github_base_branch is None:
            self.github_base_branch = "main"
        
    def create_branch(self, branch_name: str) -> str:
        """
        Creates a new branch from the working branch
        Parameters:
            branch_name(str): The name of the new branch
        Returns:
            str: A success or failure message
        """
        # check if branch exists
        try:
            self.github_repo_instance.get_branch(branch_name)
            return f"Branch {branch_name} already exists"
        except Exception as e:
            # create branch
            self.github_repo_instance.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=self.github_repo_instance.get_branch(self.github_branch).commit.sha,
            )
            self.github_branch = branch_name
            return f"Successfully created branch {branch_name}"
    
    def get_current_branch(self) -> str:
        """
        Gets the current branch
        Returns:
            str: The current branch
        """
        return self.github_branch

    def create_pull_request(self, pr_query: str) -> str:
        """
        Makes a pull request from the bot's branch to the base branch
        Parameters:
            pr_query(str): a string which contains the PR title
            and the PR body. The title is the first line
            in the string, and the body are the rest of the string.
            For example, "Updated README\nmade changes to add info"
        Returns:
            str: A success or failure message
        """
        if self.github_base_branch == self.github_branch:
            return """Cannot make a pull request because 
            commits are already in the master branch"""
        else:
            try:
                title = pr_query.split("\n")[0]
                body = pr_query[len(title) + 2 :]
                pr = self.github_repo_instance.create_pull(
                    title=title,
                    body=body,
                    head=self.github_branch,
                    base=self.github_base_branch,
                )
                return f"Successfully created PR number {pr.number}"
            except Exception as e:
                return "Unable to make pull request due to error:\n" + str(e)
    
    def file_exists(self, file_path):
        try:
            self.github_repo_instance.get_contents(file_path)
            return True
        except Exception as e:
            print(type(e))
            return False

    def create_file(self, file_path: str, file_contents: str) -> str:
        """
        Creates a new file on the Github repo
        Parameters:
            file_path (str): The path to the file to be created
            file_contents (str): The contents of the file
        Returns:
            str: A success or failure message
        """
        try:
            if not self.file_exists(file_path):
                self.github_repo_instance.create_file(
                    path=file_path,
                    message="Create " + file_path,
                    content=file_contents,
                    branch=self.github_branch,
                )
                return "Created file " + file_path
            else:
                return f"File already exists at {file_path}. Use update_file instead"
        except Exception as e:
            print(e)
            return "Unable to make file due to error:\n" + str(e)

    def read_file(self, file_path: str) -> str:
        """
        Reads a file from the github repo
        Parameters:
            file_path(str): the file path
        Returns:
            str: The file decoded as a string
        """
        try:
            file = self.github_repo_instance.get_contents(file_path)
        except Exception as e:
            print(e)
            return "Unable to read file due to error:\n" + str(e)
        return file.decoded_content.decode("utf-8")

    def update_file(self, file_path: str, file_contents: str, **kwargs) -> str:
        """
        Updates a file with new content.
        Parameters:
            file_path(str): The path to the file to be updated
            file_contents(str): The file contents.
                The old file contents is wrapped in OLD <<<< and >>>> OLD
                The new file contents is wrapped in NEW <<<< and >>>> NEW
                For example:
                /test/hello.txt
                OLD <<<<
                Hello Earth!
                >>>> OLD
                NEW <<<<
                Hello Mars!
                >>>> NEW
        Returns:
            A success or failure message
        """
        if kwargs:
            print(f"Warning: extra kwargs detected: {kwargs}")
        try:
            old_file_contents = (
                file_contents.split("OLD <<<<")[1].split(">>>> OLD")[0].strip()
            )
            new_file_contents = (
                file_contents.split("NEW <<<<")[1].split(">>>> NEW")[0].strip()
            )
            if not self.file_exists(file_path):
                return f"File does not exist at {file_path}. Use create_file instead"
            
            file_content = self.read_file(file_path)
            updated_file_content = file_content.replace(
                old_file_contents, new_file_contents
            )

            if file_content == updated_file_content:
                return (
                    "File content was not updated because old content was not found."
                    "It may be helpful to use the read_file action to get "
                    "the current file contents."
                )

            self.github_repo_instance.update_file(
                path=file_path,
                message="Update " + file_path,
                content=updated_file_content,
                branch=self.github_branch,
                sha=self.github_repo_instance.get_contents(file_path).sha,
            )
            return "Updated file " + file_path
        except IndexError:
            print(file_contents)
            return "Unable to update file because the file contents were not formatted correctly."
        except Exception as e:
            print(e)
            return "Unable to update file due to error:\n" + str(e)

    def delete_file(self, file_path: str) -> str:
        """
        Deletes a file from the repo
        Parameters:
            file_path(str): Where the file is
        Returns:
            str: Success or failure message
        """
        try:
            file = self.github_repo_instance.get_contents(file_path)
            self.github_repo_instance.delete_file(
                path=file_path,
                message="Delete " + file_path,
                branch=self.github_branch,
                sha=file.sha,
            )
            return "Deleted file " + file_path
        except Exception as e:
            print(e)
            return "Unable to delete file due to error:\n" + str(e)
    
    def run(self, function_name: str, **parameters: Dict[str, Any]) -> Any:
        if function_name == "getStatus":
            return self.get_status()
        elif function_name == "createBranch":
            return self.create_branch(**parameters)
        elif function_name == "getCurrentBranch":
            return self.get_current_branch(**parameters)
        elif function_name == "createPullRequest":
            return self.create_pull_request(**parameters)
        elif function_name == "createFile":
            return self.create_file(**parameters)
        elif function_name == "readFile":
            return self.read_file(**parameters)
        elif function_name == "updateFile":
            return self.update_file(**parameters)
        elif function_name == "deleteFile":
            return self.delete_file(**parameters)
        else:
            return "Function not found"
    
    @staticmethod
    def support(function_name: str) -> bool:
        return function_name in [
            "getStatus",
            "createBranch",
            "getCurrentBranch",
            "createPullRequest",
            "createFile",
            "readFile",
            "updateFile",
            "deleteFile",
        ]


def get_tools() -> List[Dict[str, Any]]:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "createBranch",
                "description": "Create a new branch from the working branch",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "branch_name": {
                            "type": "string", 
                            "description": "The name of the new branch"
                        },
                    },
                    "required": ["branch_name"]
                }
            }
        }, 
        {
            "type": "function",
            "function": {
                "name": "getCurrentBranch",
                "description": "Get the current github branch",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            } 
        },
        {
            "type": "function",
            "function": {
                "name": "createPullRequest",
                "description": "Make a pull request from the bot's branch to the base branch",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pr_query": {
                            "type": "string", 
                            "description": "A string which contains the PR title and the PR body. The title is the first line in the string, and the body are the rest of the string. For example, 'Updated README\nmade changes to add info'"
                        },
                    },
                    "required": ["pr_query"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "createFile",
                "description": "Create a new file on the Github repo",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string", 
                            "description": "The path to the file to be created"
                        },
                        "file_contents": {
                            "type": "string", 
                            "description": "The contents of the file"
                        },
                    },
                    "required": ["file_path", "file_contents"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "readFile",
                "description": "Read a file from the github repo",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string", 
                            "description": "The file path"
                        },
                    },
                    "required": ["file_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "updateFile",
                "description": "Update a file with new content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string", 
                            "description": "The path to the file to be updated"
                        },
                        "file_contents": {
                            "type": "string", 
                            "description": "The file contents. The old file contents is wrapped in OLD <<<< and >>>> OLD. The new file contents is wrapped in NEW <<<< and >>>> NEW. For example: /test/hello.txt OLD <<<< Hello Earth! >>>> OLD NEW <<<< Hello Mars! >>>> NEW"
                        },
                    },
                    "required": ["file_path", "file_contents"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "deleteFile",
                "description": "Delete a file from the repo",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string", 
                            "description": "Where the file is"
                        },
                    },
                    "required": ["file_path"]
                }
            }
        }
    ]
    return tools
