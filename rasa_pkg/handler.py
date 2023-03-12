import asyncio
from typing import List, Dict, Union

import yaml
from rasa.core.agent import load_agent, Agent
from rasa.model import get_local_model, get_latest_model
from rasa.model_training import train

from .utils import read_yaml_file_content, write_yaml_content_to_file

DOMAIN = "rasa_pkg/domain.yml"
DATA = "rasa_pkg/data/"
NLU = f"{DATA}nlu.yml"
CONFIG = "rasa_pkg/config.yml"
MODELS = "rasa_pkg/models/"
FAQS = "faqs/"


class Handler:
    def add_intent(self, previous_intent_name: str, intent_name: str, examples: List[str]) -> bool:
        nlu = read_yaml_file_content(NLU)
        domain = read_yaml_file_content(DOMAIN)
        intent = list(filter(lambda intent: intent == previous_intent_name, domain["intents"]))
        print(domain['intents'])
        if intent:
            #  Delete intent from  nlu file and domain file
            nlu['nlu'] = [intent for intent in nlu['nlu'] if intent['intent'] != previous_intent_name]
            domain['intents'] = [intent for intent in domain['intents'] if intent != previous_intent_name]
            # Here edit intent
            new_intent = {
                "intent": intent_name,
                "examples": yaml.dump(examples, indent=4)
            }
            nlu["nlu"] = [new_intent if intent_elm["intent"] == new_intent["intent"] else intent_elm for intent_elm in
                          nlu["nlu"]]
        else:
            nlu["nlu"].append(
                {"intent": intent_name, "examples": yaml.dump(examples, indent=4)})
            domain['intents'].append(intent_name)
        write_yaml_content_to_file(NLU, nlu)
        write_yaml_content_to_file(DOMAIN, domain)
        return True


async def _load_rasa_agent(self, model_path: str) -> Agent:
    agent = await load_agent(model_path)
    asyncio.wait(load_agent(model_path))
    return agent


async def get_model(self, name: str = None) -> Union[Agent, None]:
    if name:
        model_name = name + ".tar.gz"
        model_path = get_local_model(MODELS + model_name)
    else:
        model_path = get_latest_model(model_path=MODELS)

    if model_path:
        model = await self._load_rasa_agent(model_path)
        return model
    else:
        return None


def get_intents(self) -> List[str]:
    nlu = read_yaml_file_content(DOMAIN)
    return nlu['intents']


def get_examples_of_intent(self, intent_name: str) -> Union[Dict, None]:
    nlu = read_yaml_file_content(NLU)
    nlu_content = nlu['nlu']
    intent_examples = filter(lambda intents: intents.get(intent_name) is not None, nlu_content)
    if intent_examples:
        return {intent_name: intent_examples}
    return None


def add_new_response(self, intent_name: str, responses: List[Dict]) -> bool:
    response = read_yaml_file_content(DOMAIN)
    response['responses'].update({"utter_" + intent_name: responses})
    write_yaml_content_to_file(DOMAIN, response)
    return True


def get_responses_to_intent(self, intent_name: str) -> List[Dict]:
    content = read_yaml_file_content(DOMAIN)
    responses = content['responses']
    return responses.get('utter_' + intent_name)


def get_all_responses(self) -> list:
    content = read_yaml_file_content(DOMAIN)
    responses = content['responses']
    return responses


def add_faqs(self, intent_name: str, examples: List[str], responses: List[Dict]) -> bool:
    faq_intent = FAQS + intent_name
    self.add_intent(faq_intent, examples)
    self.add_new_response(faq_intent, responses)
    return True


def train_model(self, model_name: str):
    model_name = f"{MODELS}{model_name}"
    train(DOMAIN, CONFIG, DATA, output=model_name)
    return self.get_model(model_name)


handler = Handler()

# # Create a dictionary with the image URL and any other relevant properties
# image_dict = {
#     "image": image_url,
#     "attachment": "image",
#     "custom": {"width": "500px", "height": "300px"}
# }
