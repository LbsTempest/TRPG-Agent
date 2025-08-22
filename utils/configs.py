from dataclasses import dataclass
from ruamel.yaml import YAML

yaml = YAML()

@dataclass
class AgentConfig:
    def load_config(self, config_path: str):
        with open(config_path, 'r') as fr:
            agent_config = yaml.load(fr)
        self.base_url = agent_config["Agent"]["base_url"]
        self.api_key = agent_config["Agent"]["api_key"]