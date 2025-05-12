from openai import AsyncOpenAI

class EmbeddingClass:
    def __init__(self):
        """
        Initialize the OpenAI Embedding class.
        """
        self.openai = AsyncOpenAI()

    async def embed(self, input_text: str):
        """
        A placeholder function.

        Returns:
            type: Description of the return value.
        """
        embeddings = await self.openai.embeddings.create(
            input=input_text,
            model="text-embedding-ada-002"
        )
        return embeddings.data[0].embedding