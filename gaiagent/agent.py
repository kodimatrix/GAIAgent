from pathlib import Path
from typing import Optional

from smolagents import CodeAgent, LiteLLMModel
from smolagents.default_tools import WikipediaSearchTool


ANSWER_PROMPT = "Finish your answer with the following template: FINAL ANSWER: [YOUR FINAL ANSWER]. YOUR FINAL ANSWER should be a number OR as few words as possible OR a comma separated list of numbers and/or strings. If you are asked for a number, don't use comma to write your number neither use units such as $ or percent sign unless specified otherwise. If you are asked for a string, don't use articles, neither abbreviations (e.g. for cities), and write the digits in plain text unless specified otherwise. If you are asked for a comma separated list, apply the above rules depending of whether the element to be put in the list is a number or a string."


class Agent:
    def __init__(self):
        model = LiteLLMModel(
            model_id="ollama_chat/gemma3:4b-it-qat",
            api_base="http://localhost:11434",
            # api_key="YOUR_API_KEY",
            num_ctx=8192,
            temperature=0,
        )

        wiki = WikipediaSearchTool(
            language="en", content_type="text", extract_format="WIKI"
        )

        self.agent = CodeAgent(
            tools=[wiki],
            model=model,
            # prompt_templates=
            add_base_tools=True,
            max_steps=6,
            planning_interval=2,
            # final_answer_checks=1,
        )
        self.agent.prompt_templates["final_answer"]["post_messages"] += (
            "\n" + ANSWER_PROMPT
        )

    def __call__(
        self,
        question: str,
        file_path: Optional[Path],
    ) -> str:
        question += f"\nATTACHMENT_PATH: {file_path}"
        answer = self.agent.run(question)
        # TODO
        return answer


# agent = Agent()
# # agent("57.1*144.42=?", file_path=None)
# agent(
#     "How many studio albums were published by Mercedes Sosa between 2000 and 2009 (included)? You can use the latest 2022 version of english wikipedia.",
#     file_path=None,
# )
