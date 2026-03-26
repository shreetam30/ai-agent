from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-sonnet-20240229",
    anthropic_api_key="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"
)

print(llm.invoke("Hello"))