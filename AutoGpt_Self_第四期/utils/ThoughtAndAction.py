from typing import Optional, Dict, Any, List

from pydantic import BaseModel, Field


class Action(BaseModel):
    name: str = Field(description="工具或指令名称.")
    args: Optional[Dict[str, Any]] = Field(description="工具或指令名称.")


class Thought(BaseModel):
    text: str = Field(description="思考的内容.")
    # reasoning: str = Field(description="推理或思考的过程.")
    # plan: List[str] = Field(description="行动计划.")
    # criticism: str = Field(description="自我批判.")
    speak: str = Field(description="将思考转化为语言，作为输出.")


class ThoughtAndAction(BaseModel):
    thought: Thought = Field(description="思考过程.")
    action: Action = Field(description="当前要执行的动作.")

    def is_finish(self) -> bool:
        return self.action.name.lower() == "finish"
