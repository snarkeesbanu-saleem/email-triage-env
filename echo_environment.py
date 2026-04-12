from models import EmailTriageAction, EmailTriageObservation, EmailTriageState, EmailCategory, ActionType

class EmailTriageEnvironment:
    def __init__(self):
        self.current_task = 1
        self.scores = {}

    def reset(self):
        self.current_task = 1
        self.scores = {}
        return EmailTriageObservation(
            email_subject="Unable to login",
            email_body="Login issue",
            current_task_id=1,
            reward=0.0,
            feedback="Task 1",
            done=False
        )

    def step(self, action: EmailTriageAction):
        score = 0.8   # Simple high score for validation
        self.scores[self.current_task] = score

        if self.current_task < 3:
            self.current_task += 1
            return EmailTriageObservation(
                email_subject=f"Task {self.current_task}",
                email_body="Next task",
                current_task_id=self.current_task,
                reward=score,
                feedback=f"Task {self.current_task-1} done",
                done=False
            )
        else:
            return EmailTriageObservation(
                email_subject="Done",
                email_body="All tasks completed",
                current_task_id=3,
                reward=score,
                feedback="All tasks done",
                done=True
            )

    def state(self):
        return EmailTriageState(processed_tasks=self.scores, total_steps=len(self.scores))

    def get_grader_score(self) -> float:
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)
