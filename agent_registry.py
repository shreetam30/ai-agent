class AgentRegistry:
    def __init__(self):
        self.agents = {}

    def register(self, name, agent_card):
        self.agents[name] = agent_card

    def get(self, name):
        return self.agents.get(name)