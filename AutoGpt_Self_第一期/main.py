from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAI, OpenAIEmbeddings

from AutoGpt_Self_第一期.AutoAgent.AutoGPT import AutoGPT
from AutoGpt_Self_第一期.Tools import mocked_location_tool, weather_tool

tools = [
    mocked_location_tool,
    # calendar_tool,
    weather_tool
]


def main():
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0)
    prompt_path = "prompts"
    db = Chroma.from_documents(
        [Document(page_content="")],
        OpenAIEmbeddings(model="text-embedding-ada-002")
    )
    retriever = db.as_retriever(search_kwargs=dict(k=1))
    agent = AutoGPT(
        ai_name="gg",
        ai_role="强大的AI助手,可以使用工具与指令自动化解决问题",
        llm=llm,
        prompt_path=prompt_path,
        tools=tools,
        max_thought_steps=20,
        memory_retriever=retriever,
    )

    while True:
        task = input("有什么可以帮您: \n")
        if task.strip().lower() == "quit":
            break
        reply = agent.run(task, verbose=True)
        print(f"{agent.ai_name}: {reply}\n")


if __name__ == '__main__':
    main()
