# agent_config.py

from dataclasses import dataclass, asdict
from ruamel.yaml import YAML
from typing import Any

yaml = YAML(typ="safe")


# 对应YAML中的 Agent 节点
@dataclass
class AgentSettings:
    base_url: str
    api_key: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

# 对应包含 Agent 节点的根配置
@dataclass
class GeneralConfig:
    Agent: AgentSettings

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GeneralConfig":
        agent_data = data.get("Agent", {})
        return cls(Agent=AgentSettings(**agent_data))

    @classmethod
    def load_from_yaml(cls, config_path: str) -> "GeneralConfig":
        with open(config_path, "r", encoding="utf-8") as fr:
            config_data = yaml.load(fr)

        if config_data is None:
            raise ValueError(f"YAML file '{config_path}' is empty or invalid.")

        return cls.from_dict(config_data)


# 对应 planning_prompt 节点
@dataclass
class PlanningPromptConfig:
    initial_plan: str
    update_plan_pre_messages: str
    update_plan_post_messages: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# 对应 managed_agent_prompt 节点
@dataclass
class ManagedAgentPromptConfig:
    task: str
    report: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# 对应 final_answer_prompt 节点
@dataclass
class FinalAnswerPromptConfig:
    pre_messages: str
    post_messages: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# 对应整个YAML文件的根节点
@dataclass
class PromptConfig:
    system_prompt: str
    planning_prompt: PlanningPromptConfig
    managed_agent_prompt: ManagedAgentPromptConfig
    final_answer_prompt: FinalAnswerPromptConfig

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PromptConfig":
        """
        一个关键的辅助方法，从字典递归地创建dataclass实例。
        """
        # 递归地为嵌套的dataclass创建实例
        planning_data = data.get("planning_prompt", {})
        managed_data = data.get("managed_agent_prompt", {})
        final_answer_data = data.get("final_answer_prompt", {})

        return cls(
            system_prompt=data.get("system_prompt", ""),
            planning_prompt=PlanningPromptConfig(**planning_data),
            managed_agent_prompt=ManagedAgentPromptConfig(**managed_data),
            final_answer_prompt=FinalAnswerPromptConfig(**final_answer_data),
        )

    @classmethod
    def load_from_yaml(cls, config_path: str) -> "PromptConfig":
        """
        从YAML文件加载配置并直接返回一个配置类的实例。
        """
        with open(config_path, "r", encoding="utf-8") as fr:
            config_data = yaml.load(fr)

        if config_data is None:
            raise ValueError(f"YAML file '{config_path}' is empty or invalid.")

        return cls.from_dict(config_data)
