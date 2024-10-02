# Install necessary libraries

# Importing necessary packages
from langchain_community.document_loaders import YoutubeLoader
from langchain.tools import WikipediaQueryRun
from langchain.utilities import WikipediaAPIWrapper
from langchain.utilities import SearchApiAPIWrapper
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools, AgentExecutor, create_react_agent
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents import Tool, AgentType, initialize_agent
from langchain_groq import ChatGroq
import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn


from dotenv import load_dotenv

load_dotenv()

# Setting environment variables for API keys




# Create FastAPI app
app = FastAPI()

# Model for YouTube URL input
class YouTubeInput(BaseModel):
    url: str

# Define tools for LLM to check facts

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
serp = SearchApiAPIWrapper(searchapi_api_key = "Rnju4YsZbzjaS5tsvSZ6eTDK")
search = GoogleSearchAPIWrapper(google_api_key = "AIzaSyApGqMIzZW7zD9kvbq4HiTCbh4uDfBSJ4s", google_cse_id = "b6b75d890852a46fc" )

tools = [
    Tool(
        name="Google Search",
        description="Search Google for validating facts or claims.",
        func=search.run,
    ),
    Tool(
        name="Wikipedia",
        description="Search Wikipedia for validating facts or claims.",
        func=wikipedia.run,
    ),
    Tool(
        name="SerpAPI",
        description="Use this to get facts and verify claims.",
        func=serp.run,
    )
]

# Initialize language model
# llm = ChatOpenAI(temperature=0)  # Using GPT-3.5 turbo
groq_llm = ChatGroq(
    model="llama-3.1-70b-versatile",
    api_key="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",
    temperature=0,
)

# Customarizing the agent prompt after multiple iterations to come up with the best performing prompt, please go through it once

PREFIX = """You are a fact or claim checker. As a fact or claim checker, your responsibility is to identify and validate all the facts or claims in the Input text. Utilize all the available tools to verify these facts or claims,You must use all the tools before coming to Final Answer.

You have access to the following tools:

Google Search: Search Google for validating recent facts or claims.
Wikipedia: Search Wikepedia for validating the facts or claims.
SerpAPI: Use this to get the actual facts about the facts and verify the facts.
Google Scholar : Use this when the fact identified is related to research.


You must provide the Final Answer in the following format for each fact identified:

Fact: "Fact or claim identified from the input text after cheking each sentence.".
Validation: "True (if the Fact or claim is correct)" or "False (if the Fact or claim is wrong)"
Actual Fact: "If validation is False, state the actual fact or obtained from the sources."

You must identify facts or claims and then check using the tools. You must verify the facts or claims thoroughly using all the tools before validating.
Ensure that all Sentences are thoroughly checked and verified for facts. The output must be returned in the specified format with proper validation and the actual fact.
"True" indicates that the claim and actual fact matches from the source, "False" indicates they do not matches with each other.
Evaluate each claim and its validation using the tools before presenting the final answer. The final answer must encompass all identified claims, their respective validations, and the actual facts obtained. Your performance will be assessed based on the number of correctly identified claims and their accurate validations.
"""
FORMAT_INSTRUCTIONS = """
Use this format:
Fact: "Fact or claim from input"
Validation: "True or False"
Actual Fact: "The true fact from sources"

Use the following structure:
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Final Thought: I now know the final answer
Final Answer: the final answer to the original input question
"""
SUFFIX = """Begin!

Question: {input}
Thought:{agent_scratchpad}"""


# Initializing the agent

agent = initialize_agent(
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    tools=tools,
    llm=groq_llm,
    agent_kwargs={
        'prefix':PREFIX,
        'format_instructions':FORMAT_INSTRUCTIONS,
        'suffix':SUFFIX
    },
    handle_parsing_errors=True,
    verbose= True
)

# Define the FastAPI route
@app.post("/fact-check")
async def fact_check(input_data: YouTubeInput):
    # Extract transcript from YouTube video
    loader = YoutubeLoader.from_youtube_url(input_data.url, add_video_info=True)
    transcript = loader.load()

    # Pass transcript to the agent for fact-checking
    response = agent.run(transcript)
    
    return {"fact_check_result": response}


# Start FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
