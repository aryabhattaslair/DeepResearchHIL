# Import required modules and initialize the builder from open_deep_research
import uuid 
import os, getpass

from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver
from open_deep_research_hil.graph import builder
import asyncio

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


# Define report structure template and configure the research workflow
# This sets parameters for models, search tools, and report organization
REPORT_STRUCTURE = """Use this structure to create a report on the user-provided topic:

    1. Introduction (no research needed)
    - Brief overview of the topic area

    2. Main Body Sections:
    - Each section should focus on a sub-topic of the user-provided topic

    3. Conclusion
    - Aim for 1 structural element (either a list of table) that distills the main body sections 
    - Provide a concise summary of the report"""


async def main(thread):
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)

    # Define research topic about Model Context Protocol
    topic = "Tell me about inference time compute scaling and how that improves thinking models."

    # Run the graph workflow until first interruption (waiting for user feedback)
    async for event in graph.astream({"topic":topic,}, thread, stream_mode="updates"):
        if '__interrupt__' in event:
            interrupt_value = event['__interrupt__'][0].value
            print(interrupt_value)

    # Provide specific feedback to focus and refine the report structure
    async for event in graph.astream(Command(resume=True), thread, stream_mode="updates"):
        if '__interrupt__' in event:
            interrupt_value = event['__interrupt__'][0].value
            print(interrupt_value)

    # Approve the final plan and execute the report generation
    # This triggers the research and writing phases for all sections

    # The system will now:
    # 1. Research each section topic
    # 2. Generate content with citations
    # 3. Create introduction and conclusion
    # 4. Compile the final report
    async for event in graph.astream(Command(resume=True), thread, stream_mode="updates"):
        print(event)
        print("\n")
        
    final_state = graph.get_state(thread)
    report = final_state.values.get('final_report')
    print(report)


if __name__ == "__main__":
    # Set the API keys used for any model or search tool selections below, such as:
    #_set_env("OPENAI_API_KEY")
    #_set_env("TAVILY_API_KEY")
    #_set_env("GOOGLE_API_KEY")
    os.environ["GOOGLE_API_KEY"] = "Google API Key"
    os.environ["TAVILY_API_KEY"] = "Tavily API Key"

    # Configuration option 1: Claude 3.7 Sonnet for planning with perplexity search
    thread = {"configurable": {"thread_id": str(uuid.uuid4()),
                           "search_api": "tavily",
                           "planner_provider": "google",
                           "planner_model": "gemini-2.0-flash",
                           # "planner_model_kwargs": {"temperature":0.8}, # if set custom parameters
                           "writer_provider": "google",
                           "writer_model": "gemini-2.0-flash",
                           # "writer_model_kwargs": {"temperature":0.8}, # if set custom parameters
                           "max_search_depth": 2,
                           "report_structure": REPORT_STRUCTURE,
                           }}
    
    # Submit feedback on the report plan
    # The system will continue execution with the updated requirements
    asyncio.run(main(thread))

