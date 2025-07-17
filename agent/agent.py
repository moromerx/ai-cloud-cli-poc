from llm.llm import Session, FunctionCaller, SafetyControls
from typing import List
from llm.interfaces import ToolCallResult, LLMProvider
from typing import Union, Callable, Any
from llm.openai import OpenAIProvider
from llm.ollama import OllamaProvider
import json

class Agent:
    DEFAULT_MODELS = {
        "openai": "gpt-4o",
        "ollama": "llama3.1",
        "groq": "llama-3.3-70b-versatile"
    }
    
    PROVIDERS = {
        "openai": OpenAIProvider(),
        "ollama": OllamaProvider(),
        "groq": OpenAIProvider()
    }
    
    def __init__(
        self,
        client: Any,
        session: Session,
        model: str,
        function_caller: FunctionCaller,
        safety_controls: SafetyControls,
        tools: list,
        provider: LLMProvider,
        tool_use_behavior: Union[str, List[str], Callable[[str, Any], bool]] = "run_llm_again",
    ):
        self.client = client
        self.session = session
        self.function_caller = function_caller
        self.safety_controls = safety_controls
        self.tools = tools
        self.tool_use_behavior = tool_use_behavior
        self.provider = provider
        self.model = model
        
    def switch_provider(self, new_provider):
        if new_provider not in self.DEFAULT_MODELS:
            raise ValueError(f"Unsupported provider: {new_provider}")
        if new_provider not in self.PROVIDERS:
            raise ValueError(f"Provider {new_provider} not initialized")

        # Get new provider instance
        provider_instance = self.PROVIDERS[new_provider]

        # Rebuild client from provider instance
        if new_provider == "openai":
            client = provider_instance.build_openai_client()
        elif new_provider == "groq":
            client = provider_instance.build_groq_client()
        elif new_provider == "ollama":
            client = provider_instance.build_ollama_client()
        else:
            raise ValueError(f"No client builder defined for provider: {new_provider}")

        self.provider = new_provider
        self.model = self.DEFAULT_MODELS[new_provider]
        self.client = client
        self.provider = provider_instance
        self.session.provider = provider_instance


    def set_model(self, model_name):
        self.model = model_name
        
    def run(self, user_input: str):
        self.session.add_message("user", user_input)
        return self.agentic_loop()
    
    def should_stop_after_tool(self, tool_name: str, tool_result: Any) -> bool:
        if self.tool_use_behavior == "stop_on_first_tool":
            return True
        elif isinstance(self.tool_use_behavior, list):
            return tool_name in self.tool_use_behavior
        elif callable(self.tool_use_behavior):
            return self.tool_use_behavior(tool_name, tool_result)
        return False  # default: "run_llm_again"
    
    def agentic_loop(self):
        current_iteration = 0
        MAX_ITERATIONS = self.session.max_iterations

        while current_iteration < MAX_ITERATIONS:
            current_provider_instance = self.session.provider
            message = current_provider_instance.chat(
                client=self.client,
                model=self.model,
                messages=self.session.messages,
                tools=self.tools
            )

            self.session.messages.append(message)

            # If there are tool calls, process them and continue the loop
            if getattr(message, "tool_calls", None):
                for tool in message.tool_calls:
                    name = tool.function.name
                    args = tool.function.arguments

                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            print(f"Invalid JSON in arguments: {args}")

                    if not self.safety_controls.check(args):
                        return

                    result = self.function_caller.call(name, args)
                    tool_result = ToolCallResult(
                        result=result,
                        tool_call_id=getattr(tool, 'id', None),
                        tool_name=name
                    )
                    self.session.add_tool_response(tool_result)
                # Continue to next iteration after handling tool calls

            else:
                return (message.content.strip(), "green")

            current_iteration += 1

        return ("Max iterations reached.", "yellow")
    