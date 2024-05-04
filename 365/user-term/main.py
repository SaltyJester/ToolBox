import os
from dotenv import load_dotenv
import asyncio
from graph import Graph

load_dotenv()

# print(os.getenv('CLIENT_ID'))

async def main():
    # upn = input('Please enter UPN of user to be terminated: ')
    graph = Graph()
    user = await graph.get_user('ajones@organharvest.biz')
    print(user)
    result = await graph.block_signin(user)
    print(result)

# this is needed to prevent runtime error below, not sure why
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# this causes "RuntimeError: Event loop is closed", not sure why
asyncio.run(main()) 

# asyncio.get_event_loop().run_until_complete(main())