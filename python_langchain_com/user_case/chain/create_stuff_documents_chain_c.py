from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

from dotenv import load_dotenv

load_dotenv("../../../.env")

prompt = ChatPromptTemplate.from_messages(
    [("system", "What are everyone's favorite colors:\n\n{context}"),
     ("user", "{input}")]
)

llm = ChatOpenAI()

docs = [
    Document(page_content="Jesse loves red but not yellow"),
    Document(page_content = "Jamal loves green but not as much as he loves orange")
]

chain = create_stuff_documents_chain(llm, prompt)

p = chain.invoke({"context": docs, "input": "What are the favorite colors of Jamal?"})
print(p)