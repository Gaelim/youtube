import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.agents import Tools
from langchain.tools import DuckDuckGoSearchRun
from langchain.tools import YouTubeSearchTool
# Initialize your LLM Model
#Create an instance of OpenAI LLM
llm = ChatOpenAI(model_name='gpt-3.5-turbo',openai_api_key="your api key" ,temperature=0.0)

# build a tool to search the internet
search = DuckDuckGoSearchRun()
yt = YouTubeSearchTool()
searh_tool = Tool(name="search_tool", description = "search the net",func = search.run)
yt_tool= Tool( name='Youtube', description="search youtube videos",func= yt.run)
tools = [search_tool,yt_tool]

#build our agent
agent = initialize_agent(tools, llm, agent='zero-shot-react-description',verbose=True)

st.title(' GPT tester')
# Create a text input box for the user
#Create a  Propmt 
prompt =  st.text_input('Input your prompt here')


# If user hits enter
if prompt:
    #then pass the prompt to the llm
    response =agent.run(prompt)
    #and write out tot the screen 
    st.write(response)