from langchain_ollama import ChatOllama


from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
# from langchain_core.pydantic_v1 import BaseModel, Field # Probably issue 
# from langchain_openai import ChatOpenAI
from typing import Optional

from pydantic import BaseModel, Field

llm = ChatOllama(model="deepseek-r1:14b", temparature=0)
# llm = ChatOllama(model="llama3.2:3b", temparature=0)
# llm_json_mode = ChatOllama(model="deepseek-r1:14b", temparature=0,format='json')

topic = "Lion"

joke_query = f"Tell me a joke about {topic}, nothing else, nothing more."


msg = llm.invoke(joke_query)

print("#################### regular call###################")
print(msg.content)


print("#############################################")
print("#################### json mode call###################")




# # Pydantic
# class Joke(BaseModel):
#     """Joke to tell user."""

#     setup: str = Field(description="The setup of the joke")
#     punchline: str = Field(description="The punchline to the joke")
#     rating: Optional[int] = Field(
#         default=None, description="How funny the joke is, from 1 to 10"
#     )


# structured_llm = llm.with_structured_output(Joke)

# print(structured_llm.invoke("Tell me a joke about cats"))

# Define your desired data structure.
class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")
    explaination: str = Field(description="explanantion why it is funny")


# And a query intented to prompt a language model to populate the data structure.


# Set up a parser + inject instructions into the prompt template.
parser = JsonOutputParser(pydantic_object=Joke)



prompt = PromptTemplate(
    template="Answer the user query.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | llm | parser

msg = chain.invoke({"query": joke_query})


print("#######")
print(type(msg))
print(msg)
print("##############################################")

chain = prompt | llm 

msg = chain.invoke({"query": joke_query})
print(type(msg.content))
print(msg.content)