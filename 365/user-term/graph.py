import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder
from msgraph.generated.models.user import User

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
        query_params = UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
            # select isn't working as I expected, need to dig into it more
            # select = ["displayName"],
            filter = f"userPrincipalName eq '{upn}'"
        )

        request_configuration = UsersRequestBuilder.UsersRequestBuilderGetRequestConfiguration(
            query_parameters = query_params,
        )

        user = await self.client.users.get(request_configuration = request_configuration)
        # user = await self.client.users.get()
        return user.value[0]

    async def block_signin(self, user: User):
        request_body = User(
            account_enabled = False
        )

        result = await self.client.users.by_user_id(user.id).patch(request_body)
        return result
