from cloud_cli import CloudCLI
from ui.ui import UI
from rich.console import Console
from tools.tools import tools
from agent.agent import Agent
from llm.llm import SafetyControls, Session, FunctionCaller
from llm.openai import OpenAIProvider
from dotenv import load_dotenv

def main():
    system_prompt = """
        
        # Identity

        You are an agent designed to write and execute Python code using the `boto3` library to answer AWS-related questions. You operate in a Python execution environment that has valid AWS credentials and access to a tool called `run_python_code`, which runs Python code in an isolated REPL and returns the printed output or error messages.
        
        # Instructions
        
        ## Instructions:
        - Examine current state of AWS resources relevant to user's query.
        - Analyze the query, previous reasoning steps, and observations.
        - Reflect on 5-7 different ways to solve the given query or task. Think carefully about each solution before picking the best one. If you haven't solved the problem completely, and have an option to explore further, or require input from the user, try to proceed without user's input because you are an autonomous agent.
        - Decide on the next action: use a tool or provide a final answer.

        ## Remember:
        - Fetch current state of AWS resources relevant to user's query.
        - Prefer the tool usage that does not require any interactive input.
        - Use tools when you need more information. Do not respond with the instructions on how to use the tools or what commands to run, instead just use the tool.
        - Provide a final answer only when you're confident you have sufficient information.
        - Provide clear, concise, and accurate responses.
        - Feel free to respond with emojis where appropriate.
        """
        
    load_dotenv()
    console = Console()
    MAX_ITERATIONS = 5

    ui = UI(console)

    # Start with default provider (openai)
    current_provider = OpenAIProvider()
    client = current_provider.build_openai_client()
    default_model = "gpt-4o"
    
    session = Session(
        system_prompt=system_prompt,
        max_iterations=MAX_ITERATIONS,
        provider=current_provider
    )
    
    function_caller = FunctionCaller()
    safety_controls = SafetyControls(ui)

    agent = Agent(
        client=client,
        session=session,
        model=default_model,
        function_caller=function_caller,
        safety_controls=safety_controls,
        tools=tools,
        provider=current_provider,
    )

    app = CloudCLI(agent, ui)
    app.run()

if __name__ == "__main__":
    main()