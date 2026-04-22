from models import EmailTriageAction, EmailTriageObservation, EmailTriageState, ActionType, EmailCategory
from typing import Dict, Any

class EmailTriageEnvironment:
    def __init__(self):
        self.current_task = 1
        self.scores = {}
        self.task_ground_truth = {
            1: {
                "subject": "Cannot login to dashboard",
                "body": "Hi, I've been trying to login to the company dashboard for an hour. It says 'invalid credentials' even after password reset. Please help urgently.",
                "expected": {
                    "category": "support",
                    "priority": "high",
                    "action_type": ActionType.REPLY
                }
            },
            2: {
                "subject": "Billing discrepancy",
                "body": "My invoice for March shows $299 but I was charged $349. Please check and refund the difference. Not urgent but need resolution.",
                "expected": {
                    "category": "complaint",
                    "priority": "medium",
                    "action_type": ActionType.ESCALATE
                }
            },
            3: {
                "subject": "Feature request: Dark mode",
                "body": "Love the product! Would be great to have dark mode for late night work. Just a suggestion for future roadmap.",
                "expected": {
                    "category": "internal",
                    "priority": "low",
                    "action_type": ActionType.ARCHIVE
                }
            }
        }

    def reset(self):
        self.current_task = 1
        self.scores = {}
        task = self.task_ground_truth[1]
        return EmailTriageObservation(
            email_subject=task["subject"],
            email_body=task["body"],
            current_task_id=1,
            reward=0.0,
            feedback="Task 1 started. Please classify and decide action.",
            done=False
        )

    def _grade_action(self, action: EmailTriageAction, task_id: int) -> float:
        """Grade the agent's action against ground truth."""
        expected = self.task_ground_truth[task_id]["expected"]
        score = 0.0
        
        # Category match (40% weight)
        if action.category == expected["category"]:
            score += 0.4
        
        # Priority match (30% weight)
        if action.priority == expected["priority"]:
            score += 0.3
        
        # Action type match (30% weight)
        if action.action_type == expected["action_type"]:
            score += 0.3
        
        return score

    def step(self, action: EmailTriageAction):
        # Grade the action for current task
        score = self._grade_action(action, self.current_task)
        self.scores[self.current_task] = score
        
        # Prepare feedback
        expected = self.task_ground_truth[self.current_task]["expected"]
        feedback = f"Task {self.current_task} graded {score:.2f}. "
        if score < 1.0:
            feedback += f"Expected: category={expected['category']}, priority={expected['priority']}, action={expected['action_type'].value}."
        
        if self.current_task < 3:
            self.current_task += 1
            task = self.task_ground_truth[self.current_task]
            return EmailTriageObservation(
                email_subject=task["subject"],
                email_body=task["body"],
                current_task_id=self.current_task,
                reward=score,
                feedback=feedback,
                done=False
            )
        else:
            # Last task completed
            return EmailTriageObservation(
                email_subject="All tasks completed",
                email_body="Thanks for processing all emails.",
                current_task_id=3,
                reward=score,
                feedback=feedback + " All tasks completed.",
                done=True
            )

    def state(self):
        return EmailTriageState(
            processed_tasks=self.scores,
            total_steps=len(self.scores)
        )

    def get_grader_score(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)
