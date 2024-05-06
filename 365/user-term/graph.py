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
            select = ["id", "userPrincipalName", "displayName", "accountEnabled"],
            filter = f"userPrincipalName eq '{upn}'"
        )

        request_configuration = UsersRequestBuilder.UsersRequestBuilderGetRequestConfiguration(
            query_parameters = query_params,
        )

        user = await self.client.users.get(request_configuration = request_configuration)
        
        # user.value == 1, since we're only looking for one user at a time
        return user.value[0]

    def print_user_attr(self, user):
        for attr, value in vars(user).items():
            if(value != None):
                print(attr, ':', value)

    async def block_signin(self, user):
        request_body = User(
            account_enabled = False
        )
        result = await self.client.users.by_user_id(user.id).patch(request_body)

        # Checking to make sure that user's sign in was disabled
        user = await self.get_user(user.user_principal_name)
        if user.account_enabled:
            # at some point, we may want to throw an error here instead
            return False
        return True

    async def reset_password(self, user):
        # 