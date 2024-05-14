import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from azure.identity import DeviceCodeCredential
from msgraph.generated.users.users_request_builder import UsersRequestBuilder
from msgraph.generated.groups.groups_request_builder import GroupsRequestBuilder
from msgraph.generated.models.user import User
from msgraph.generated.models.password_profile import PasswordProfile
import string
import secrets

load_dotenv()

class Graph:
    def __init__(self):
        self.device_code_credential = DeviceCodeCredential(os.getenv('CLIENT_ID'), tenant_id = os.getenv('TENANT_ID'))

        # credential = ClientSecretCredential(
        #     tenant_id=os.getenv('TENANT_ID'),
        #     client_id=os.getenv('CLIENT_ID'),
        #     client_secret=os.getenv('CLIENT_SECRET')
        # )

        # scopes = ['https://graph.microsoft.com/.default']
        scopes = ['Directory.AccessAsUser.All']

        self.client = GraphServiceClient(credentials=self.device_code_credential, scopes=scopes)

    async def get_user(self, upn):
        query_params = UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
            select = ["id", "userPrincipalName", "displayName", "accountEnabled", "lastPasswordChangeDateTime"],
            filter = f"userPrincipalName eq '{upn}'"
        )

        request_configuration = UsersRequestBuilder.UsersRequestBuilderGetRequestConfiguration(
            query_parameters = query_params,
        )

        user = await self.client.users.get(request_configuration = request_configuration)
        
        # user.value == 1, since we're only looking for one user at a time
        return user.value[0]

    async def get_user_groups(self, user):
        query_params = GroupsRequestBuilder.GroupsRequestBuilderGetQueryParameters(
            select = ["id","displayName","groupTypes","classification","mailEnabled","membershipRule","mail"]
        )

        request_configuration = GroupsRequestBuilder.GroupsRequestBuilderGetRequestConfiguration(
            query_parameters = query_params,
        )
        # groups = await self.client.users.by_user_id(user.id).member_of.get()
        groups = await self.client.users.by_user_id(user.id).member_of.get(request_configuration = request_configuration)

        return groups.value

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
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(16))

        request_body = User(
            password_profile = PasswordProfile(
                force_change_password_next_sign_in = False,
		        password = password,
            )
        )
        
        try:
            result = await self.client.users.by_user_id(user.id).patch(request_body)
        except Exception as e:
            print(e)

        # verifying to see if password was changed
        updated_user = await self.get_user(user.user_principal_name)
        if(not (user.last_password_change_date_time < updated_user.last_password_change_date_time)):
            return False

        return True

    async def remove_group_membership(self, user, groups):
        for group in groups:
            await self.client.groups.by_group_id(group.id).members.by_directory_object_id(user.id).ref.delete()
        return True
