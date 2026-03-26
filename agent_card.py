class AgentCard:
    def __init__(self, name, agent):
        self.name = name
        self.agent = agent

    def send(self, message: str):
        print(f"\n🔁 {self.name} Agent RECEIVED: {message}")
        
        response = self.agent.run(message)
        
        print(f"✅ {self.name} Agent RESPONSE: {response['output']}\n")
        
        return response