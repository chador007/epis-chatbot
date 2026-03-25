from services.chunking_service import ChunkingService

service = ChunkingService()
text = "my name is chador wangchuk and i work as software developer at epis. Tashi is newly recruited as AI developer this month."
chunks = service.chunk(text)
print(chunks)