from models import EmailTriageAction, EmailTriageObservation, EmailTriageState, EmailCategory, ActionType

class EmailTriageEnvironment:
    def __init__(self):
        self.tasks = {
            1: {  # Easy
                "subject": "Unable to login to company portal",
                "body": "Hi team, I keep getting 'invalid credentials' when trying to login. Please help.",
                "gt_category": EmailCategory.SUPPORT,
                "gt_priority": "high",
                "gt_action": ActionType.REPLY
            },
            2: {  # Medium
                "subject": "Request for enterprise pricing details",
                "body": "Hello, Our company with 40 employees is interested in your enterprise plan. Can you share pricing?",
                "gt_category": EmailCategory.SALES,
                "gt_priority": "medium",
                "gt_action": ActionType.REPLY
            },
            3: {  # Hard
                "subject": "Very disappointed with delayed delivery",
                "body": "I ordered 5 days ago and still not received. This is unacceptable. I want immediate refund or replacement!",
                "gt_category": EmailCategory.COMPLAINT,
                "gt_priority": "high",
                "gt_action": ActionType.REPLY
            }
        }
        self.current_task = 1
        self.processed = {}
        self.step_count = 0

    def reset(self):
        self.current_task = 1
        self.processed = {}
        self.step_count = 0
        task = self.tasks[1]
        return EmailTriageObservation(
            email_subject=task["subject"],
            email_body=task["body"],
            current_task_id=1,
            reward=0.0
        )

    def step(self, action: EmailTriageAction):
        self.step_count += 1
        
        if action.task_id != self.current_task:
            return EmailTriageObservation(
                email_subject="Error",
                email_body="Incorrect task_id",
                current_task_id=self.current_task,
                reward=-0.3,
                feedback="Task ID mismatch"
            )

        gt = self.tasks[action.task_id]
        score = 0.0
        if action.category == gt["gt_category"]:
            score += 0.35
        if action.priority == gt["gt_priority"]:
            score += 0.3
        if action.action_type == gt["gt_action"]:
            score += 0.35

        # Bonus for good reply
        if action.action_type == ActionType.REPLY and action.reply_text:
            if len(action.reply_text) > 40:
                score += 0.15

        reward = min(score, 1.0)

        self.processed[action.task_id] = reward

        feedback = f"Task {action.task_id} score: {reward:.2f}"

        if self.current_task < 3:
            self.current_task += 1
            next_task = self.tasks[self.current_task]
            obs = EmailTriageObservation(
                email_subject=next_task["subject"],
                email_body=next_task["body"],
                current_task_id=self.current_task,
                reward=reward,
                feedback=feedback
            )
            done = False
        else:
            obs = EmailTriageObservation(
                email_subject="All tasks completed",
                email_body="",
                current_task_id=action.task_id,
                reward=reward,
                done=True,
                feedback=feedback
            )
            done = True

        return obs

    def state(self):
        return EmailTriageState(
            processed_tasks=self.processed,
            total_steps=self.step_count
        )

    def get_grader_score(self) -> float:
        if not self.processed:
            return 0.0
        return sum(self.processed.values()) / len(self.processed)