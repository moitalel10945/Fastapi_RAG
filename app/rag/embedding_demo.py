from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

model = SentenceTransformer("all-MiniLM-L6-v2")

sentence1 = "How do I register a tenant?"
sentence2 = "How can I add a new tenant?"
sentence3 = "How do I generate a rent report?"

embedding1 = model.encode(sentence1)
embedding2 = model.encode(sentence2)
embedding3 = model.encode(sentence3)

similarity12 = cos_sim(embedding1, embedding2)
similarity13 = cos_sim(embedding1, embedding3)

print(f"Sentence 1: {sentence1}")
print(f"Sentence 2: {sentence2}")
print(f"Similarity: {similarity12.item():.4f}")

print()

print(f"Sentence 1: {sentence1}")
print(f"Sentence 3: {sentence3}")
print(f"Similarity: {similarity13.item():.4f}")