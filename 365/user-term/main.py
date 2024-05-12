import asyncio
from graph import Graph

# print(os.getenv('CLIENT_ID'))

async def main():
    # upn = input('Please enter UPN of user to be terminated: ')
    graph = Graph()
    user = await graph.get_user('ajones@organharvest.biz')
    graph.print_user_attr(user)
    
    # Block Sign in
    result = await graph.block_signin(user)
    print(result)

    # Reset Password
    print(await graph.reset_password(user))

# this is needed to prevent runtime error below, not sure why
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# this causes "RuntimeError: Event loop is closed", not sure why
asyncio.run(main()) 