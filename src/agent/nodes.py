from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain import hub
from dotenv import load_dotenv
import os


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')


def analyze_documents(state) -> Literal["generate", "summarize"]:
    """Determine if the retrieved documents are sufficient to answer the user's question."""
    print("---CHECKING RELEVANCE---")

    class Score(BaseModel):
        binary_score: str = Field(description="Relevance Score 'yes' or 'no'")

    model = ChatOpenAI(temperature=0, model="gpt-4o-mini", streaming=True)
    llm_with_tools = model.with_structured_output(Score)

    prompt = PromptTemplate(
        template="""You are an evaluator assessing the relevance of a retrieved document to a user's question.\n
        Here is the retrieved document:\n\n{context}\n\n
        Here is the user's question: {question}\n
        If the document contains keyword(s) or semantic meaning related to the user's question, classify it as relevant.\n
        Return a binary score 'yes' or 'no' to indicate whether the document is relevant to the question.""",
        input_variables=["context", "question"],
    )

    pipeline = prompt | llm_with_tools

    messages = state["messages"]
    question = messages[0].content
    docs = messages[-1].content

    evaluated = pipeline.invoke({"question": question, "context": docs})
    score_val = evaluated.binary_score

    if score_val == "yes":
        print("---DECISION: DOCUMENTS ARE RELEVANT---")
        return "generate"
    else:
        print("---DECISION: DOCUMENTS ARE NOT RELEVANT---")
        return "rewrite"


def agent(state, tools):
    print("---Calling AGENT---")
    messages = state["messages"]
    model = ChatOpenAI(temperature=0, model="gpt-4o-mini", streaming=True)
    model = model.bind_tools(tools)
    response = model.invoke(messages)
    return {"messages" :[response]}

def rewrite(state):
    """Rewrite the user's question to be more specific."""
    print("---Rewriting Question---")
    messages = state["messages"]
    question = messages[0].content

    model = ChatOpenAI(temperature=0, model="gpt-4o-mini", streaming=True)

    msgs = [
        SystemMessage(content="Rewrite the user question to be more specific and detailed. Output only the rewritten question."),
        HumanMessage(content=question) 
    ]

    ai_msg = model.invoke(msgs)

    return {"messages": [ai_msg]}

def generate(state):
    """Generate the final answer."""
    print("---GENERATING---")
    messages = state["messages"]
    question = messages[0].content
    docs = messages[-1].content

    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0, streaming=True)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = prompt | llm | StrOutputParser()
    answer = rag_chain.invoke({"context": docs, "question": question})
    return {"messages": [answer]}