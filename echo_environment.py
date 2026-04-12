from models import EmailTriageAction, EmailTriageObservation, EmailTriageState, EmailCategory, ActionType

class EmailTriageEnvironment:
    def __init__(self):
        self.current_task = 1
        self.scores = {}
        self.steps = 0

        self.tasks = {
            1: {"name": "easy_support", "subject": "Login issue", "body": "Cannot login to dashboard", "category": EmailCategory.SUPPORT, "priority": "high", "action": ActionType.REPLY},
            2: {"name": "medium_sales", "subject": "Enterprise pricing", "body": "Need pricing for 40 users", "category": EmailCategory.SALES, "priority": "medium", "action": ActionType.REPLY},
            3: {"name": "hard_complaint", "subject": "Delayed delivery complaint", "body": "Order delayed, want refund", "category": EmailCategory.COMPLAINT, "priority": "high", "action": ActionType.REPLY}
        }

    def reset(self):
        self.current_task = 1
        self.scores = {}
        self.steps = 0
        t = self.tasks[1]
        return EmailTriageObservation(
            email_subject=t["subject"],
            email_body=t["body"],
            current_task_id=1,
            reward=0.0,
            feedback="Task 1 started",
            done=False
        )

    def step(self, action: EmailTriageAction):
        self.steps += 1
        t = self.tasks[self.current_task]

        score = 0.0
        if action.category == t["category"]: score += 0.4
        if action.priority == t["priority"]: score += 0.3
        if action.action_type == t["action"]: score += 0.3

        if action.reply_text and len(action.reply_text) > 20:
            score += 0.2

        reward = min(score, 1.0)
        self.scores[self.current_task] = reward

        if self.current_task < 3:
            self.current_task += 1
            next_t = self.tasks[self.current_task]
            return EmailTriageObservation(
                email_subject=next_t["subject"],
                email_body=next_t["body"],
                current_task_id=self.current_task,
                reward=reward,
                feedback=f"Task {self.current_task-1} score: {reward:.2f}",
                done=False
            )
        else:
            return EmailTriageObservation(
                email_subject="All tasks completed",
                email_body="",
                current_task_id=self.current_task,
                reward=reward,
                feedback=f"Final score: {reward:.2f}",
                done=True
            )

    def state(self):
        return EmailTriageState(processed_tasks=self.scores, total_steps=self.steps)

    def get_grader_score(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)
