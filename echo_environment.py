from models import EmailTriageAction, EmailTriageObservation, EmailTriageState, EmailCategory, ActionType

class EmailTriageEnvironment:
    def __init__(self):
        self.current_task_id = 1
        self.processed_scores = {}
        self.total_steps = 0

        # Explicit 3 tasks with graders
        self.tasks = {
            1: {
                "name": "support_login",
                "subject": "Unable to login to company portal",
                "body": "Hi team, I keep getting 'invalid credentials' when trying to login. Please help.",
                "gt_category": EmailCategory.SUPPORT,
                "gt_priority": "high",
                "gt_action": ActionType.REPLY
            },
            2: {
                "name": "sales_pricing",
                "subject": "Request for enterprise pricing details",
                "body": "Hello, Our company with 40 employees is interested in your enterprise plan. Can you share pricing?",
                "gt_category": EmailCategory.SALES,
                "gt_priority": "medium",
                "gt_action": ActionType.REPLY
            },
            3: {
                "name": "complaint_refund",
                "subject": "Very disappointed with delayed delivery",
                "body": "I ordered 5 days ago and still not received. This is unacceptable. I want immediate refund or replacement!",
                "gt_category": EmailCategory.COMPLAINT,
                "gt_priority": "high",
                "gt_action": ActionType.REPLY
            }
        }

    def reset(self):
        self.current_task_id = 1
        self.processed_scores = {}
        self.total_steps = 0
        task = self.tasks[1]
        return EmailTriageObservation(
            email_subject=task["subject"],
            email_body=task["body"],
            current_task_id=1,
            reward=0.0,
            feedback=f"Started task 1: {task['name']}",
            done=False
        )

    def step(self, action: EmailTriageAction):
        self.total_steps += 1

        if action.task_id != self.current_task_id:
            return EmailTriageObservation(
                email_subject="Error",
                email_body="Incorrect task_id",
                current_task_id=self.current_task_id,
                reward=-0.3,
                feedback="Task ID mismatch",
                done=False
            )

        gt = self.tasks[action.task_id]
        score = 0.0

        if action.category == gt["gt_category"]:
            score += 0.4
        if action.priority == gt["gt_priority"]:
            score += 0.3
        if action.action_type == gt["gt_action"]:
            score += 0.3

        if action.action_type == ActionType.REPLY and action.reply_text and len(action.reply_text.strip()) > 30:
            score += 0.2

        reward = min(score, 1.0)
        self.processed_scores[action.task_id] = reward

        if self.current_task_id < 3:
            self.current_task_id += 1
            next_task = self.tasks[self.current_task_id]
            obs = EmailTriageObservation(
                email_subject=next_task["subject"],
                email_body=next_task["body"],
                current_task_id=self.current_task_id,
                reward=reward,
                feedback=f"Task {action.task_id} completed with score {reward:.2f}",
                done=False
            )
        else:
            obs = EmailTriageObservation(
                email_subject="All tasks completed",
                email_body="",
                current_task_id=action.task_id,
                reward=reward,
                feedback=f"Final task completed with score {reward:.2f}",
                done=True
            )

        return obs

    def state(self):
        return EmailTriageState(
            processed_tasks=self.processed_scores,
            total_steps=self.total_steps
        )

    def get_grader_score(self) -> float:
        if not self.processed_scores:
            return 0.0
        return sum(self.processed_scores.values()) / len(self.processed_scores)

    # Extra method to make graders more visible to validator
    def get_task_grader(self, task_id: int):
        if task_id in self.processed_scores:
            return self.processed_scores[task_id]
        return 0.0
