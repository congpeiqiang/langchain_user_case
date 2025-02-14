from typing import List, Optional

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, VectorStoreRetrieverMemory
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_core.language_models import BaseLLM, BaseChatModel
from langchain_core.tools import BaseTool
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import OpenAI
from llama_index_client import ValidationError

from AutoGpt_Self_第一期.utils.PromptTemplateBuilder import PromptTemplateBuilder
from AutoGpt_Self_第一期.utils.ThoughtAndAction import ThoughtAndAction


def format_thought(thought):
    def format_plans(plans: List[str]):
        ans = ""
        for plan in plans:
            ans += f"- {plan}\n"
        return ans.strip()

    ans = (
        "\n"
        f"思考： {thought.text}\n"
        # f"推理： {thought.reasoning}\n"
        # f"计划： {format_plans(thought.plan)}\n"
        # f"反思: {thought.criticism}\n"
        f"输出: {thought.speak}\n"
        "\n"
    )
    return ans


def format_action(action):
    ans = f"{action.name}("
    if action.args is None or len(action.args) == 0:
        ans += ")"
        return ans
    for k, v in action.args.items():
        ans += f"{k}={v},"
    ans = ans[:-1] + ")"
    return ans


class AutoGPT:
    """ 基于langchain的实现"""

    def __init__(
            self,
            llm: BaseLLM | BaseChatModel,
            prompt_path: str,
            tools: List[BaseTool],
            ai_name: Optional[str] = "瓜瓜",
            ai_role: Optional[str] = "强大的AI助手,可以使用工具与指令自动化解决问题",
            max_thought_steps: Optional[int] = 0,
            memory_retriever: Optional[VectorStoreRetriever] = None,

    ):
        self.llm = llm
        self.prompt_path = prompt_path
        self.tools = tools
        self.ai_name = ai_name
        self.ai_role = ai_role
        self.max_thought_steps = max_thought_steps
        self.memory_retriever = memory_retriever

        self.output_parser = PydanticOutputParser(
            pydantic_object=ThoughtAndAction
        )

        self.step_prompt = PromptTemplateBuilder(
            self.prompt_path,
            "step_instructions.templ"
        ).build().format()

        self.force_rethink_prompt = PromptTemplateBuilder(
            self.prompt_path,
            "force_rethink.templ"
        ).build().format()

    def run(self, task_description, verbose=False) -> str:
        thought_step_count = 0
        print(f"thought_step_count: {thought_step_count}")
        prompt_template = PromptTemplateBuilder(
            self.prompt_path
        ).build(
            tools=self.tools,
            output_parser=self.output_parser
        ).partial(
            ai_name=self.ai_name,
            ai_role=self.ai_role,
            task_description=task_description
        )

        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        short_term_memory = ConversationBufferWindowMemory(
            ai_prefix="Reason",
            human_prefix="Act",
            k=self.max_thought_steps,
        )

        summary_memory = ConversationSummaryMemory(
            llm=OpenAI(temperature=0),
            buffer="问题: " + task_description + "\n",
            ai_prefix="Reason",
            human_prefix="Act",
        )

        if self.memory_retriever is not None:
            long_term_memory = VectorStoreRetrieverMemory(
                retriever=self.memory_retriever
            )
        else:
            long_term_memory = None

        reply = ""
        finish_turn = False
        last_action = None
        while thought_step_count < self.max_thought_steps:
            thought_and_action = self._step(
                chain=chain,
                task_description=task_description,
                short_term_memory=short_term_memory,
                long_term_memory=long_term_memory
            )

            if finish_turn:
                self._final_step(
                    short_term_memory,
                    task_description)
                break

            action = thought_and_action.action
            if self.is_repeat(last_action, action):
                self._step(
                    chain=chain,
                    task_description=task_description,
                    short_term_memory=short_term_memory,
                    long_term_memory=long_term_memory,
                    force_rethink=True
                )
                action = thought_and_action.action
            last_action = action

            if verbose:
                print(format_thought(thought_and_action.thought))

            if thought_and_action.is_finish():
                finish_turn = True
                break

            tool = self._find_tool(action.name)
            if tool is None:
                result = (
                    f"Error, 找不到工具或指令, '{action.name}'."
                    f"请从提供的工具和列表中选择, 请确保按对应格式输出。"
                )
            else:
                try:
                    observation = tool.run(action.args)
                except ValidationError as e:
                    observation = (
                        f"ValidationError: in args: {str(e)}, args:{action.args}"
                    )
                except:
                    observation = (
                        f"Error: {str(e)}, {type(e).__name__}, args:{action.args}"
                    )
                result = (
                    f"执行: {format_action(action)}\n"
                    f"返回结果：{observation}"
                )
            if verbose:
                print(result)
            short_term_memory.save_context(
                {"input": format_thought(thought_and_action.thought)},
                {"output": result}
            )
            if long_term_memory is not None:
                summary_memory.save_context(
                    {"input": format_thought(thought_and_action.thought)},
                    {"output": format_action(action)}
                )

            thought_step_count += 1
            reply = thought_and_action.thought.speak
        if long_term_memory is not None:
            long_term_memory.save_context(
                {"input": task_description},
                {"output": summary_memory.load_memory_variables({})["history"]}
            )
        return reply

    def _step(self,
              chain,
              task_description,
              short_term_memory,
              long_term_memory,
              force_rethink=None
              ):
        current_response = chain.run(
            short_term_memory=short_term_memory.load_memory_variables({})["history"],
            long_term_memory=long_term_memory.load_memory_variables(
                {"prompt": task_description}
            )["history"] if long_term_memory is not None else "",
            step_instructions=self.step_prompt if force_rethink is False else self.force_rethink_prompt
        )
        print(f"current_response: {current_response}")
        robust_parser = OutputFixingParser.from_llm(
            parser=self.output_parser,
            llm=self.llm
        )
        thought_and_action = robust_parser.parse(current_response)
        return thought_and_action

    def is_repeat(self, last_action, action):
        if last_action is None:
            return False
        if last_action.name != action.name:
            return False
        if last_action.args is None and action.args is None:
            return True
        if last_action.args is not None or action.args is None:
            return False
        for k, v in last_action.args.items():
            if k not in action.args:
                return False
            if action.args[k] != v:
                return False
        return True

    def _final_step(self, short_term_memory, task_description):
        finish_prompt = PromptTemplateBuilder(
            self.prompt_path,
            "finish_instructions.templ"
        ).build(
            tools=self.tools,
            output_parser=self.output_parser
        ).partial(
            ai_name=self.ai_name,
            ai_role=self.ai_role,
            task_description=task_description,
            short_term_memory=short_term_memory.load_memory_variables({})["history"]
        )
        chain = LLMChain(llm=self.llm, prompt=finish_prompt)
        response = chain.run({})
        return response

    def _find_tool(self, name):
        for tool in self.tools:
            if tool.name == name:
                return tool
        return None
