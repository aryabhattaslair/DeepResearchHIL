import getpass
import os
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

#from langchain_google_genai import ChatGoogleGenerativeAI


def main():
    '''
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,ß
        max_tokens=None,
        timeout=None,ß
        max_retries=2,
    )
    messages = [
        (
            "system",
            "You are a helpful assistant that translates English to French. Translate the user sentence.",
        ),
        ("human", "I love programming."),
    ]
    ai_msg = llm.invoke(messages)
    return ai_msg
    '''
    # Define the desired structure
    class Person(BaseModel):
        """Information about a person."""

        name: str = Field(..., description="The person's name")
        height_m: float = Field(..., description="The person's height in meters")

    # Initialize the model
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    structured_llm = llm.with_structured_output(Person)

    # Invoke the model with a query asking for structured information
    result = structured_llm.invoke(
        "Who was the 16th president of the USA, and how tall was he in meters?"
    )
    print(result)


async def run_async_calls(llm):
    # Async invoke
    result_ainvoke = await llm.ainvoke("Why is the sky blue?")
    print("Async Invoke Result:", result_ainvoke.content[:50] + "...")

    # Async stream
    print("\nAsync Stream Result:")
    async for chunk in llm.astream("Write a short poem about asynchronous programming."):
        print(chunk.content, end="", flush=True)
    
    print("\n")

    # Async batchßßß
    results_abatch = await llm.abatch(["What is 1+1?", "What is 2+2?"])
    print("Async Batch Results:", [res.content for res in results_abatch])


async def main_async():
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    await run_async_calls(llm)


if __name__ == "__main__":
    # Set the API key for Google Gemini
    os.environ["GOOGLE_API_KEY"] = "Google_API_Key"
    #print(main())
    asyncio.run(main_async())
    