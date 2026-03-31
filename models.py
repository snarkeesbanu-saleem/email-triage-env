from pydantic import BaseModel
from typing import Literal, Optional, Dict
from enum import Enum

class EmailCategory(str, Enum):
    SUPPORT = 'support'
    SALES = 'sales'
    COMPLAINT = 'complaint'
    SPAM = 'spam'
    INTERNAL = 'internal'

class ActionType(str, Enum):
    REPLY = 'reply'
    ARCHIVE = 'archive'
    ESCALATE = 'escalate'
    FORWARD = 'forward'

class EmailTriageAction(BaseModel):
    task_id: int
    category: EmailCategory
    priority: Literal['low', 'medium', 'high']
    action_type: ActionType
    reply_text: Optional[str] = None

class EmailTriageObservation(BaseModel):
    email_subject: str
    email_body: str
    current_task_id: int
    feedback: Optional[str] = None
    done: bool = False
    reward: float = 0.0

class EmailTriageState(BaseModel):
    processed_tasks: Dict[int, float]
    total_steps: int
