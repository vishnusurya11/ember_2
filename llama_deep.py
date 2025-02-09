from langchain_ollama import ChatOllama


from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from typing import Optional

from pydantic import BaseModel, Field

llm = ChatOllama(model="deepseek-r1:14b", temparature=0)
# llm = ChatOllama(model="llama3.2:3b", temparature=0)


topic = "Lion"

joke_query = f"Tell me a joke about {topic}, nothing else, nothing more."


class Joke(BaseModel):
    setup: str = Field(description="question to set up a joke")
    punchline: str = Field(description="answer to resolve the joke")
    explaination: str = Field(description="explanantion why it is funny")




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
