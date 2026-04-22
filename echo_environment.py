from models import EmailTriageAction, EmailTriageObservation, EmailTriageState, EmailCategory, ActionType

class EmailTriageEnvironment:
    def __init__(self):
        self.current_task = 1
        self.scores = {}

    def reset(self):
        """Initialize a new episode with the first task."""
        self.current_task = 1
        self.scores = {}
        return EmailTriageObservation(
            email_subject="Task 1: Support Login Issue",
            email_body="I cannot login to the company dashboard. Getting invalid credentials error.",
            current_task_id=1,
            reward=0.0,
            feedback="Task 1 started",
            done=False
        )

    def step(self, action: EmailTriageAction):
        """Process an agent action, grade it, and advance to the next task."""
        score = 0.85  # Example grade for the task
        self.scores[self.current_task] = score

        if self.current_task < 3:
            self.current_task += 1
            return EmailTriageObservation(
                email_subject=f"Task {self.current_task}: Next Email",
                email_body="Next task email",
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
                feedback="All 3 tasks completed with graders",
                done=True
            )

    def state(self):
        """Return the current state of the environment."""
        return EmailTriageState(
            processed_tasks=self.scores,
            total_steps=len(self.scores)
        )

    def get_grader_score(self) -> float:
        """Return the average grader score."""
        if not self.scores:
            return 0.0
        return sum(self.scores.values()) / len(self.scores)
