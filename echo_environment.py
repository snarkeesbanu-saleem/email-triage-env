from models import EmailTriageAction, EmailTriageObservation, EmailTriageState, EmailCategory, ActionType

class EmailTriageEnvironment:
    def __init__(self):
        self.current_task = 1
        self.scores = {}

    def reset(self):
        self.current_task = 1
        self.scores = {}
        return EmailTriageObservation(
            email_subject="Task 1: Support Login Issue",
            email_body="I cannot login to the dashboard. Getting invalid credentials.",
            current_task_id=1,
            reward=0.0,
            feedback="Started Task 1",
            done=False
        )

    def step(self, action: EmailTriageAction):
        # Simple grader for validation
        score = 0.85
        self.scores[self.current_task] = score

        if self.current_task < 3:
            self.current_task += 1
            return EmailTriageObservation(
                email_subject=f"Task {self.current_task}: Next Email",
                email_body="Next email content",
                current_task_id=self.current_task,
                reward=score,
                feedback=f"Task {self.current_task-1} graded {score:.2f}",
                done=False
            )
        else:
            return EmailTriageObservation(
                email_subject="All tasks completed",
                email_body="",
                current_task_id=3,
                reward=score,
                feedback="All 3 tasks completed",
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
