import requests
from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()

# ['url',
#  'repository_url',
#  'labels_url',
#  'comments_url',
#  'events_url',
#  'html_url',
#  'id',
#  'node_id',
#  'number',
#  'title',
#  'user',
#  'labels',
#  'state',
#  'locked',
#  'assignee',
#  'assignees',
#  'milestone',
#  'comments',
#  'created_at',
#  'updated_at',
#  'closed_at',
#  'author_association',
#  'active_lock_reason',
#  'draft',
#  'pull_request',
#  'body',
#  'closed_by',
#  'reactions',
#  'timeline_url',
#  'performed_via_github_app',
#  'state_reason']
@dataclass
class GitHubIssue:
    number: int
    title: str
    body: str
    state: str
    comments: int
    created_at: str
    updated_at: str

def get_issues(owner:str, repo:str):
    token = os.getenv("GITHUB_TOKEN") 
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {"Authorization": f"token {token}"}

    response = requests.get(url, headers=headers)
    issues = response.json()
    github_issues = [
        GitHubIssue(
            number=issue["number"],
            title=issue["title"],
            comments=issue["comments"],
            created_at=issue["created_at"],
            updated_at=issue["updated_at"],
            body=issue["body"],
            state=issue["state"]
        )
        for issue in issues  #if "pull_request" not in issue
    ]

    return github_issues


# if __name__ == "__main__":
#     github_issues = get_issues("iluwatar", "java-design-patterns")

#     for gi in github_issues:
#         print(f"Issue #{gi.number}: [{gi.state}] {gi.title} ")