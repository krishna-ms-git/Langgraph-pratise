#Generates outline and Blog on any give topic

from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from langchain_ollama import ChatOllama

model = ChatOllama(model="llama3.2:latest")

#define state
class BlogPost(TypedDict):
    topic: str
    outline: str
    content: str

#node functions
def gen_outline(state:BlogPost) -> BlogPost:
    
    #fetch topic from user
    topic = state['topic']
    
    #pass promt to LLM
    prompt = f'Generate detaialed outline on topic -{topic}'
    outline = model.invoke(prompt).content
    
    #update state
    state['outline'] = outline
    return state

def gen_blog(state:BlogPost) -> BlogPost:
    
    #fetch topic and outline
    topic = state['topic']
    outline = state ['outline']
    
    #generate prompt with above
    prompt = f'Generate a blog post with details from topic: {topic} using outline:{outline}'
    
    #pass outline to LLM 
    blog_content = model.invoke(prompt).content
    
    #update state
    state['content'] = blog_content
    return state
    
    
#define graph
graph = StateGraph(BlogPost)

#add nodes and edges
graph.add_node('gen_outline', gen_outline)
graph.add_node('gen_blog', gen_blog)

graph.add_edge(START, 'gen_outline')
graph.add_edge('gen_outline', 'gen_blog')
graph.add_edge('gen_blog', END)

#compile graph
workflow = graph.compile()

#execute graph
initial_state = {'topic': 'Raise of AI in India'}
final_state = workflow.invoke(initial_state)

print(final_state['outline'])
print(final_state['content'])
