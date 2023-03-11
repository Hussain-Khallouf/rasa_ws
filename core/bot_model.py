import asyncio

from rasa.core.agent import Agent
from rasa.core.channels import UserMessage

from core.base import Singleton
from rasa_pkg.handler import handler


class BotModel(Singleton):
    model: Agent = None
    _response = None

    def __init__(self, model_name=None):
        super().__init__()
        self.set_model(model_name)

    async def _set_model(self, model_name):
        self.model = await handler.get_model(model_name)

        return True

    def set_model(self, model_name):
        asyncio.run(self._set_model(model_name))

    def train(self, model_name):
        self.model = handler.train_model(model_name)
        return True

    async def _set_response(self, message: UserMessage):
        self._response = await self.model.handle_message(message)

    def get_response(self, message: UserMessage):
        asyncio.run(self._set_response(message))
        print(self._response)
        return self._response[0]["text"]


bot_model = BotModel()
