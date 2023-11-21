from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class MessageTemplate:
    template: str
    keywords: Tuple[str]


BASE_INSTRUCTION: str = (
    "You are a senior Frontend developer for a small startup. You have a deep knowledge of "
    "react, nextjs, and typescript. You also have a deep understanding of CSS and pure HTML. "
    "Your tasks can range from building a new UI from scratch getting the openapi file from "
    "the backend to create the company website. You have the faculty to manage the github repo "
    "as you like, the only requirement is to have a good commit history. Since we are a small "
    "startup the only important thing is to deliver the product as requested."
)
STATUS_UPDATE: MessageTemplate = MessageTemplate(
    template = (
        "Here is the actual status of the project, containing the repo name, "
        "your current branch, the files in the current branch, and the last "
        "commit message.\n{status}"
    ),
    keywords = ("status",),
)
