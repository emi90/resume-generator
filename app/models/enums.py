from enum import Enum


class OutputFormat(str, Enum):
    MARKDOWN = "markdown"
    TEXT = "text"


class ResumeSource(str, Enum):
    FILE = "file"
    TEXT = "text"


class JobSource(str, Enum):
    URL = "url"
    TEXT = "text"
