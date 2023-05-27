from github import Github


class CodeReviewer:
    def __call__(self, code):
        return [(1, 'This is a comment')]


class GithubAPI:
    def __init__(self, access_token):
        self.g = Github(access_token)
        self.code_reviewer = CodeReviewer()
    
    def write_comments_for_pr(self, repo_name, pr_number):
        repo = self.g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        files = pr.get_files()
        for file in files:
            if file.status == 'added' or file.status == 'modified':
                comments = self.code_reviewer(file.patch)
                for position, comment in comments:
                    pr.create_review_comment(body=comment, commit_id=pr.head.sha, path=file.filename, position=position)
        return 200


if __name__ == '__main__':
    import os
    
    api = GithubAPI(os.environ['GITHUB_ACCESS_TOKEN'])
    api.write_comments_for_pr('diegofiori/generative-playground', 1)
    