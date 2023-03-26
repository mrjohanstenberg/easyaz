import azure.identity
import easyaz.openai

my_azure_openai_endpoint = 'https://someinstance.openai.azure.com'

creds = azure.identity.DefaultAzureCredential()
easyaz.openai.login(my_azure_openai_endpoint, credential=creds)

import openai

embeddings = openai.Embedding.create(deployment_id = '<some deployment id>', input="Simple, no?")
print(embeddings)