import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import EmailTriageAction
from echo_environment import EmailTriageEnvironment

app = FastAPI(title="Email Triage Environment - Scaler x Meta Hackathon")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

env = EmailTriageEnvironment()

@app.post('/reset')
async def reset():
    obs = env.reset()
    return obs.model_dump()

@app.post('/step')
async def step(action: EmailTriageAction):
    obs = env.step(action)
    return obs.model_dump()

@app.get('/tasks')
async def list_tasks():
    return {
        'tasks': [1, 2, 3],
        'description': 'Real-world Email Triage (Easy → Medium → Hard)',
        'action_schema': EmailTriageAction.model_json_schema()
    }

@app.post('/grader')
async def get_grader_score():
    score = env.get_grader_score()
    return {'grader_score': round(score, 3)}

@app.get('/baseline')
async def baseline():
    return {'baseline_score': 0.78, 'message': 'Reproducible baseline'}
