import json
import os
import tempfile
from typing import Optional, List

from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import load_prompt
from langchain_core.tools import BaseTool

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
                 prompt_file: str = "main.json",
                 ):
        self.prompt_path = prompt_path,
        self.prompt_file = prompt_file

    def build(self,
              tools: Optional[List[BaseTool]] = None,
              output_parser: Optional[BaseOutputParser] = None,
              ) -> PromptTemplate:
        print(os.path.join(self.prompt_path, self.prompt_file))
        main_file = os.path.join(self.prompt_path[0], self.prompt_file)
        main_templ_template = load_prompt(
            self._check_or_redirect(main_file)
        )
        partial_variables = {}
        for var in main_templ_template.input_variables:
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
        return main_templ_template.partial(**partial_variables)

    def _check_or_redirect(self, prompt_file):
        with open(prompt_file, "r", encoding="utf-8") as f:
            config = json.load(f)
        if "template_path" in config:
            # 如果是相对路径，则转换为绝对路径
            if not os.path.isabs(config["template-path"]):
                config["template_path"] = os.path.join(self.prompt_path, config["template_path"])
            # 生成临时文件
            tmp_file = tempfile.NamedTemporaryFile(
                suffix='.json',
                mode ="w",
                encoding="utf-8",
                delete=False,
            )
            tmp_file.write(json.dumps(config, ensure_ascii=False))
            tmp_file.close()
            return tmp_file.name
        return prompt_file

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
