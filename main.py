import json
from pathlib import Path
import typer
import logging

from gaiagent.evaluation_api import EvaluationAPI

DATA_DIR = Path("data")
FILES_DIR = DATA_DIR / "files"
QUESTIONS_FP = DATA_DIR / "questions.json"
ANSWERS_FP = DATA_DIR / "answers.json"

app = typer.Typer()


@app.command()
def download():
    DATA_DIR.mkdir(exist_ok=True)
    FILES_DIR.mkdir(exist_ok=True)

    api = EvaluationAPI()
    questions = api.questions()
    QUESTIONS_FP.write_text(json.dumps(questions, indent=2))
    typer.echo(
        f"⬇  Saved {len(questions)} questions to {QUESTIONS_FP.relative_to('.')}"
    )

    for q in questions:
        fname = q.get("file_name")
        if not fname:
            continue
        tid = q["task_id"]
        target_dir = FILES_DIR / tid
        target_dir.mkdir(exist_ok=True)
        file_path = target_dir / fname
        logging.info("• Downloading attachment for %s …", tid)
        file_bytes = api.fetch_file(tid)
        file_path.write_bytes(file_bytes)

    typer.echo("✅  Download step finished.")


if __name__ == "__main__":
    app()
