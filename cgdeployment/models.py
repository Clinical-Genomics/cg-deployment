from typing import Optional, List

from pydantic import BaseModel


class Payload(BaseModel):
    class Config:
        extra = "allow"


class ReleasePayload(Payload):
    action: Optional[str]
    changes: Optional[Payload]
    issue: Optional[Payload]
    release: Optional[dict]


class IssueCommentsPayload(Payload):
    action: Optional[str]
    changes: Optional[Payload]
    issue: Optional[Payload]
    comment: Optional[Payload]


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
