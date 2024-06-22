import uvicorn
import asyncio

from http_client import HTTPClient
from storage_model import Storage
from user_model import UserModel
from h_service import HamsterService, HamsterBotTaskMorseService, HamsterBotTaskCardService
from connection_manager import ConnectionManager
from log import logger
from schemas import MorseHamsterSchema, UsersSchema

from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


async def get_storage():
    return Storage()

async def get_http_client():
    return HTTPClient()

async def get_users():
    return [
        {'token': '', 'proxy': {'http': ''}}
    ]

responses = []
flag = True

@asynccontextmanager
async def lifespan(app: FastAPI):
    storage = await get_storage()
    http_client = await get_http_client()
    users = await get_users()
    asyncio.create_task(process_data(storage, http_client, users, flag))
    yield

app = FastAPI(lifespan=lifespan)
manager = ConnectionManager()

async def process_data(
    storage: Storage, 
    http_client: HTTPClient, 
    users: UsersSchema, 
    flag
) -> None:
    while flag:
        for user_data in users:
            user = UserModel(**user_data)
            hamster_service = HamsterService(storage, http_client, user)
            response = hamster_service.proccess()
            responses.append(response)
        await asyncio.sleep(600)


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
):
    await manager.connect(websocket)
    try:
        while True:
            await manager.broadcast(responses)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post('/morse')
def morse(
    morse: MorseHamsterSchema, 
    users = Depends(get_users),
    http_client = Depends(get_http_client)
    ):
    for i_user in users:
        user = UserModel(**i_user)
        task = HamsterBotTaskMorseService(http_client, user, morse)
        response = task.morse_run()
        responses.append(response)

@app.post('/card_update')
def card_update(
    users = Depends(get_users),
    storage = Depends(get_storage),
    http_client = Depends(get_http_client)
):
    for i_data_user in users:
        user = UserModel(**i_data_user)
        hamster_card_service = HamsterBotTaskCardService(http_client, user, storage)
        response = hamster_card_service.process()
        responses.append(response)


@app.get('/users')
def users_all(
    users = Depends(get_users)
):
    users_tokens = [UsersSchema(i_user['token'][:30]) for i_user in users]
    return users_tokens


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)