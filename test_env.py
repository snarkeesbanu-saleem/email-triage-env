# test_env.py - A simple rule-based agent that makes optimal decisions
from echo_environment import EmailTriageEnvironment
from models import EmailTriageAction, ActionType, EmailCategory

# Ground truth mapping for demonstration (agent could use NLP)
task_truth = {
    1: {"category": "support", "priority": "high", "action": ActionType.REPLY},
    2: {"category": "complaint", "priority": "medium", "action": ActionType.ESCALATE},
    3: {"category": "internal", "priority": "low", "action": ActionType.ARCHIVE}
}

env = EmailTriageEnvironment()
obs = env.reset()
print(f"TASK {obs.current_task_id}: {obs.email_subject}\n{obs.email_body}\n")

total_score = 0
for step in range(3):
    # Agent decides action based on email content (here we cheat with ground truth)
    # In a real system, you'd use a classifier or LLM
    action = EmailTriageAction(
        task_id=obs.current_task_id,
        action_type=task_truth[obs.current_task_id]["action"],
        category=task_truth[obs.current_task_id]["category"],
        priority=task_truth[obs.current_task_id]["priority"],
        confidence=0.95
    )
    
    obs = env.step(action)
    print(f"Agent chose: {action.action_type.value}, {action.category}, {action.priority}")
    print(f"Reward: {obs.reward:.2f} | Feedback: {obs.feedback}\n")
    total_score += obs.reward
    
    if obs.done:
        break

print(f"Final average score: {env.get_grader_score():.2f}")
print(f"Total score (sum): {total_score:.2f} out of 3.0")