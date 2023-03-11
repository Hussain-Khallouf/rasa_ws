from typing import List

from core.utils import get_rasa_handler
from nlu.models import Intent


def add_intent_to_bot(intent_name: str, examples: List[str], **kwargs):
    print(examples)
    handler = get_rasa_handler()
    handler.add_intent(intent_name=intent_name, examples=examples)
