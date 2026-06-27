from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_ollama import ChatOllama


model = ChatOllama(model="llama3.2:latest")

#define state type for the workflow
class LLMAsk(TypedDict):
    question: str
    answer: str
    
#define the AskQuestion node
def AskQuestion(state: LLMAsk) -> LLMAsk:
    #extract the question from the state
    question = state['question']
    
    #form the prompt for the LLM
    prompt = f"Answer the following question: {question}"
    
    #ask the LLM for an answer to the question
    answer = model.invoke(prompt).content  # assuming model.invoke returns an object with a 'content' attribute
    
    #update the state with the answer from the LLM
    state['answer'] = answer
    return state

#define the workflow graph
graph = StateGraph(LLMAsk)

graph.add_node('Qa', AskQuestion)

graph.add_edge(START, 'Qa')
graph.add_edge('Qa',END)

#compile the graph into a workflow

workflow = graph.compile()

#execute workflow

initial_state = ({'question': "What is the capital of South Africa"})
final_state = workflow.invoke(initial_state)

print(final_state)

    