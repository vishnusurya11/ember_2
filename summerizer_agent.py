from typing import List, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from summerizer_chains import( 
 summary_generate_chain,
 summary_reflect_chain,
 new_summary_generate_chain,
 new_summary_reflect_chain,

)
# Constants
MAX_ITERATIONS= 6

SUMMARY_PROMPT_REFLECT = "summary_prompt_reflect"
SUMMARY_PROMPT_GENERATE = "summary_prompt_generate"

NEW_SUMMARY_PROMPT_REFLECT = "new_summary_prompt_reflect"
NEW_SUMMARY_PROMPT_GENERATE = "new_summary_prompt_generate"



# Helper functions
def summary_generation_node(state: Sequence[BaseMessage]):
    return summary_generate_chain.invoke({"messages": state})

def summary_reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = summary_reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]

def new_summary_generation_node(state: Sequence[BaseMessage]):
    return new_summary_generate_chain.invoke({"messages": state})

def new_summary_reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = new_summary_reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]

# Function to process input content and return the final response
def summary_prompt_generating_agent(input_content: str) -> str:
    # Initialize the graph builder
    builder = MessageGraph()
    builder.add_node(SUMMARY_PROMPT_GENERATE, summary_generation_node)
    builder.add_node(SUMMARY_PROMPT_REFLECT, summary_reflection_node)
    builder.set_entry_point(SUMMARY_PROMPT_GENERATE)

    # Conditional edge function
    def should_continue(state: List[BaseMessage]):
        print(f" in iteration : {len(state)}")
        if len(state) > MAX_ITERATIONS:
            return END
        return SUMMARY_PROMPT_REFLECT

    builder.add_conditional_edges(SUMMARY_PROMPT_GENERATE, should_continue)
    builder.add_edge(SUMMARY_PROMPT_REFLECT, SUMMARY_PROMPT_GENERATE)
    graph = builder.compile()

    # Create input message
    inputs = HumanMessage(content=input_content)

    # Invoke the graph with the input message
    response = graph.invoke(inputs)

    print("#########################################")
    print(response)
    print("#########################################")

    # Return the final response content
    return response[-1].content


def new_summary_prompt_generating_agent(input_content: str) -> str:
    # Initialize the graph builder
    builder = MessageGraph()
    builder.add_node(NEW_SUMMARY_PROMPT_GENERATE, new_summary_generation_node)
    builder.add_node(NEW_SUMMARY_PROMPT_REFLECT, new_summary_reflection_node)
    builder.set_entry_point(NEW_SUMMARY_PROMPT_GENERATE)

    # Conditional edge function
    def should_continue(state: List[BaseMessage]):
        print(f" in iteration : {len(state)}")
        if len(state) > MAX_ITERATIONS:
            return END
        return NEW_SUMMARY_PROMPT_REFLECT

    builder.add_conditional_edges(NEW_SUMMARY_PROMPT_GENERATE, should_continue)
    builder.add_edge(NEW_SUMMARY_PROMPT_REFLECT, NEW_SUMMARY_PROMPT_GENERATE)
    graph = builder.compile()

    # Create input message
    inputs = HumanMessage(content=input_content)

    # Invoke the graph with the input message
    response = graph.invoke(inputs)

    print("#########################################")
    print(response)
    print("#########################################")

    # Return the final response content
    return response[-1].content

# Example usage
if __name__ == "__main__":

    def read_story(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return {"story": file.read()}

    # Example usage
    input_dict = read_story('chapter_3.txt')
    # print(input_dict)


    input_text = f"""for the below novel/chapter generate a summary 
    Story : {input_dict['story']}
 
                """
    print("####################################################")
    generated_sumamry = summary_prompt_generating_agent(input_text)
    print(f"generated_sumamry ---> {generated_sumamry}")
    print("####################################################")
    new_generated_sumamry = new_summary_prompt_generating_agent(input_text)
    print(f"new_generated_sumamry ---> {new_generated_sumamry}")
    print("####################################################")