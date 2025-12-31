# Prompt

class PromptBuilder:
    def build_prompt(self, query, documents):
        context = "\n".join([doc.page_content for doc in documents])
        prompt = f""" Your are a helpful assistant.
        Use the following context to answer the question.

        Context:
        {context}
        
        Question: 
        {query}

        Answer:
        """
        return prompt