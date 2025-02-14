import json
import os
from typing import Optional, List

from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.tools import BaseTool

from AutoGpt_Self_第一期.utils.FileUtils import load_file
from langchain.prompts import PromptTemplate

from AutoGpt_Self_第一期.utils.ThoughtAndAction import ThoughtAndAction


# os.environ['http_proxy'] = 'http://127.0.0.1:7890'
# os.environ['https_proxy'] = 'http://127.0.0.1:7890'
# os.environ['OPENAI_API_KEY'] = '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'

def chinese_friendly(string) -> str:
    lines = string.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('{') and line.endswith('{'):
            try:
                lines[1] = json.dumps(json.loads(line), ensure_ascii=False)
            except:
                pass
    return '\n'.join(lines)


class PromptTemplateBuilder:
    def __init__(self,
                 prompt_path: str,
                 prompt_file: str = "main.templ",
                 ):
        self.prompt_path = prompt_path,
        self.prompt_file = prompt_file

    def build(self,
              tools: Optional[List[BaseTool]] = None,
              output_parser: Optional[BaseOutputParser] = None,
              ) -> PromptTemplate:
        print(os.path.join(self.prompt_path[0], self.prompt_file))
        main_templ_str = load_file(
            os.path.join(self.prompt_path[0], self.prompt_file)
        )
        main_templ = PromptTemplate.from_template(template=main_templ_str)
        partial_variables = {}
        for var in main_templ.input_variables:
            if var.endswith("_templ"):
                var_file = var[:-6] + ".templ"
                var_str = self._get_prompt(var_file)
                partial_variables[var] = var_str

        if tools is not None:
            tools_prompt = self._get_tools_prompt(tools)
            partial_variables["tools"] = tools_prompt

        if output_parser is not None:
            partial_variables["format_instructions"] = chinese_friendly(
                output_parser.get_format_instructions()
            )
        return main_templ.partial(**partial_variables)

    def _get_prompt(self, var_file):
        builder = PromptTemplateBuilder(self.prompt_path[0], var_file)
        return builder.build().format()

    def _get_tools_prompt(self, tools):
        tools_prompt = ""
        for i, tool in enumerate(tools):
            prompt = f"{i + 1}. {tool.name}:{tool.description}, \"" \
                     f"arg json schema:{json.dumps(tool.args, ensure_ascii=False)}\n"
            tools_prompt += prompt
        return tools_prompt


if __name__ == '__main__':
    builder = PromptTemplateBuilder(prompt_path=r"/AutoGpt_Self_第一期\prompts")
    output_parser = PydanticOutputParser(
        pydantic_object=ThoughtAndAction
    )
    prompt = builder.build(output_parser=output_parser)
    print(prompt.format(
        ai_name="瓜瓜",
        ai_role="强大的AI助手,可以使用工具与指令自动化解决问题",
        format_instructions="format_instructions",
        task_description="task_description",
        tools="tools",
        long_term_memory="",
        short_term_memory="",
        step_instructions="",
    ))
