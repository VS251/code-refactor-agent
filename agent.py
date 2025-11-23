from langchain_ollama import ChatOllama
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tools import read_file, write_file, validate_syntax, search_codebase

llm = ChatOllama(
    model="llama3.1",
    temperature=0.1, 
)

tools = [read_file, write_file, validate_syntax, search_codebase]

system_prompt = (
    "You are an Autonomous Code Refactoring Engine. "
    "Your goal is to read a file, improve the code, and save it."
    "\n\n"
    "STRICT PROCESS:"
    "\n1. Call `read_file(file_path)` to get the content."
    "\n2. **INTERNAL THOUGHT**: In your own mind, rewrite the code to satisfy the user request. DO NOT call a tool for this."
    "\n3. Call `write_file(file_path, content)` with the **FULL, COMPLETE** new code."
    "\n\n"
    "CRITICAL RULES:"
    "\n- `read_file` ONLY accepts `file_path`. Do not pass code or instructions to it."
    "\n- Do not output the code to the user. You MUST save it to the file."
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True
)

def run_agent(user_input: str):
    try:
        enhanced_input = f"{user_input} -> FINAL STEP: You MUST save the new code to the file using write_file."
        result = agent_executor.invoke({"input": enhanced_input})
        return result['output']
    except Exception as e:
        return f"Agent Error: {e}"