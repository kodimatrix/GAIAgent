from typing import TypedDict
import requests


class Answer(TypedDict):
    task_id: str
    submitted_answer: str


class EvaluationAPI:
    BASE = "https://agents-course-unit4-scoring.hf.space"

    def __init__(self, timeout: float = 15):
        self.session = requests.Session()
        self.timeout = timeout

    def questions(self) -> list[dict]:
        r = self.session.get(f"{self.BASE}/questions", timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def fetch_file(self, task_id: str) -> bytes:
        r = self.session.get(f"{self.BASE}/files/{task_id}", timeout=self.timeout)
        r.raise_for_status()
        return r.content

    def submit(self, username: str, code_url: str, answers: list[Answer]) -> dict:
        payload = {
            "username": username.strip(),
            "agent_code": code_url,
            "answers": answers,
        }
        r = self.session.post(f"{self.BASE}/submit", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()
