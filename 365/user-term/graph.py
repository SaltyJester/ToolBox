import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient

class Graph:
    def __init__(self):
        credential = ClientSecretCredential(
            tenant_id=os.getenv('TENANT_ID'),
            client_id=os.getenv('CLIENT_ID'),
            client_secret=os.getenv('CLIENT_SECRET')
        )

        scopes = ['https://graph.microsoft.com/.default']

        self.client = GraphServiceClient(credentials=credential, scopes=scopes)

    async def get_user(self, upn):
        user = await self.client.users.by_user_id(upn).get()
        return user
