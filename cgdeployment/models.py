import datetime
from typing import Optional, List, Any

from pydantic import BaseModel


class Payload(BaseModel):
    class Config:
        extra = "allow"


class PullRequestObjectPayload(Payload):
    url: Optional[str]
    html_url: Optional[str]
    diff_url: Optional[str]
    patch_url: Optional[str]


class UserObjectPayload(Payload):
    login: Optional[str]
    id: Optional[int]
    node_id: Optional[str]
    avatar_url: Optional[str]
    gravatar_id: Optional[str]
    url: Optional[str]
    html_url: Optional[str]
    followers_url: Optional[str]
    following_url: Optional[str]
    gists_url: Optional[str]
    starred_url: Optional[str]
    subscriptions_url: Optional[str]
    organizations_url: Optional[str]
    repos_url: Optional[str]
    events_url: Optional[str]
    received_events_url: Optional[str]
    type: Optional[str]
    site_admin: Optional[bool]


class IssueObjectPayload(Payload):
    id: Optional[int]
    comments: Optional[int]
    updated_at: Optional[datetime.datetime]
    number: Optional[int]
    labels_url: Optional[str]
    body: Optional[str]
    closed_at: Optional[datetime.datetime]
    labels: Optional[List]
    author_association: Optional[str]
    repository_url: Optional[str]
    milestone: Optional[Any]
    assignee: Optional[Any]
    pull_request: Optional[PullRequestObjectPayload]
    performed_via_github_app: Optional[Any]
    user: Optional[UserObjectPayload]
    comments_url: Optional[str]
    title: Optional[str]
    assignees: Optional[List]
    state: Optional[str]
    html_url: Optional[str]
    events_url: Optional[str]
    url: Optional[str]
    locked: Optional[bool]
    active_lock_reason: Optional[Any]
    node_id: Optional[str]
    created_at: Optional[datetime.datetime]


class CommentObjectPayload(Payload):
    performed_via_github_app: Optional[Any]
    user: Optional[UserObjectPayload]
    updated_at: Optional[datetime.datetime]
    issue_url: Optional[str]
    id: Optional[int]
    body: Optional[str]
    html_url: Optional[str]
    url: Optional[str]
    author_association: Optional[str]
    node_id: Optional[str]
    created_at: Optional[datetime.datetime]


class RepositoryObjectPayload(Payload):
    id: Optional[int]
    name: Optional[str]
    full_name: Optional[str]
    url: Optional[str]
    default_branch: Optional[str]


class ReleasePayload(Payload):
    action: Optional[str]
    changes: Optional[Payload]
    issue: Optional[Payload]
    release: Optional[dict]


class IssueCommentsPayload(Payload):
    action: Optional[str]
    changes: Optional[Payload]
    issue: Optional[IssueObjectPayload]
    comment: Optional[CommentObjectPayload]
    sender: Optional[UserObjectPayload]
    repository: Optional[RepositoryObjectPayload]


class IssuesPayload(Payload):
    action: Optional[str]
    changes: Optional[Payload]
    issue: Optional[Payload]
    assignee: Optional[Payload]
    label: Optional[Payload]


class PullRequestPayload(Payload):
    action: Optional[str]
    number: Optional[int]
    changes: Optional[Payload]
    pull_request: Optional[Payload]


class PushPayload(Payload):
    push_id: Optional[int]
    size: Optional[int]
    distinct_size: Optional[int]
    ref: Optional[str]
    head: Optional[str]
    before: Optional[str]
    commits: Optional[List[Payload]]
