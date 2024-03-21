
from promptflow import tool
from promptflow.connections import AzureOpenAIConnection
import os

from pyrit.agent import RedTeamingBot
from pyrit.chat import AzureOpenAIChat
from pyrit.chat.aml_online_endpoint_chat import AMLOnlineEndpointChat
from pyrit.chat_message_normalizer import GenericSystemSquash
from pyrit.common import default_values
from pyrit.models import ChatMessage



# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(pyrit_modelname:str, 
                pyrit_connection: AzureOpenAIConnection, 
                agent_modelname:str,
                agent_connection: AzureOpenAIConnection, 
                objective: str,
                metaprompt: str,
                ) -> str:



    conversation_objective = (
        objective
    )
    conversation_objective = str(conversation_objective)  # Convert tuple to string

    # The adversarial_bot is the used to generate prompts that are sent to the target
    # In this case, it's a custom deployed AML endpoint
    # In this example, our endpoint disallows system prompts, so we create the endpoint as follows
    #chat_engine = AMLOnlineEndpointChat(chat_message_normalizer=GenericSystemSquash())
    chat_engine = AzureOpenAIChat(
        deployment_name=pyrit_modelname,
        endpoint=pyrit_connection.api_base,
        api_key=pyrit_connection.api_key,
    )

    adversarial_bot = RedTeamingBot(conversation_objective=conversation_objective, chat_engine=chat_engine)

    target_bot = AzureOpenAIChat(
        deployment_name=agent_modelname,
        endpoint=agent_connection.api_base,
        api_key=agent_connection.api_key,
    )


    objective_achieved = False
    target_bot_response = "how can I help you?"
    attempts = 0
    max_attempts = 5
    multi_turn_messages = []
    system_message = ChatMessage(role="system", content=metaprompt)
    multi_turn_messages.append(system_message)
    
    while not objective_achieved and attempts < max_attempts:
        adversarial_bot_message = adversarial_bot.complete_chat_user(message=target_bot_response)

        if adversarial_bot.is_conversation_complete():
            print(f"Adversarial bot has completed the conversation and achieved the objective.")
            break
        
        print(f"#### Attempt #{attempts}")
        print(f"#### Sending the following to the target bot: {adversarial_bot_message}")
        print()

        multi_turn_messages.append(ChatMessage(role="user", content=adversarial_bot_message))

        target_bot_response = target_bot.complete_chat(messages=multi_turn_messages)

        print(f"Response from target bot: {target_bot_response}")
        multi_turn_messages.append(ChatMessage(role="assistant", content=target_bot_response))

        attempts += 1
        
    if multi_turn_messages and multi_turn_messages[-1].content:
        return {'output': multi_turn_messages[-1].content}
    else:
        return {'output': ''}
