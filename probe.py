from foundry_local import FoundryLocalManager
from openai import OpenAI

ALIAS = "qwen3-embedding-0.6b"

manager = FoundryLocalManager(ALIAS)
print("endpoint:", manager.endpoint)

info = manager.get_model_info(ALIAS)
print("model id:", info.id)

client = OpenAI(base_url=manager.endpoint, api_key=manager.api_key or "not-needed")

resp = client.embeddings.create(
    model=info.id,
    input=["Merhaba dunya", "RAG nedir?"],
)

print("kac vektor:", len(resp.data))
print("vektor boyutu:", len(resp.data[0].embedding))
print("ilk 5 sayi:", resp.data[0].embedding[:5])
