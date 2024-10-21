import logging
from time import sleep
from celery import shared_task

from .cache import get_conversation_id
from .models import Document, ChatConversation, convert_conversation_to_openai_messages
from .brain import openai_chat_complete, get_embedding, gen_doc_prompt
from .configs import DEFAULT_COLLECTION_NAME
from .vectorize import search_vector

logger = logging.getLogger(__name__)



def create_or_update_chat_conversation(bot_id, user_id, message):
    # Step 1: Create a new ChatConversation instance
    conversation_id = get_conversation_id(bot_id, user_id)

    new_conversation = ChatConversation(
        conversation_id=conversation_id,
        bot_id=bot_id,
        user_id=user_id,
        message=message,
        is_request=True,
        completed=False,
    )
    # Step 4: Save the ChatConversation instance
    new_conversation.save()

    logger.info(f"Create message for conversation {conversation_id}")

    return conversation_id

def detect_user_intent(bot_id, user_id, message):
    # load history
    # call openai --> intent user
    return message


@shared_task()
def answer_user_request(bot_id, user_id, message):
    # Update chat conversation
    conversation_id = create_or_update_chat_conversation(bot_id, user_id, message)

    # Sub task
    user_intent = detect_user_intent(bot_id, user_id, message)

    # Embedding text
    vector = get_embedding(user_intent)
    logger.info(f"Get vector of input {message}")

    # Search document
    top_docs = search_vector(DEFAULT_COLLECTION_NAME, vector, 4)
    logger.info(f"Top docs: {top_docs}")

    # Convert history to list messages
    openai_messages = convert_conversation_to_openai_messages(conversation_id)

    # Update documents to prompt
    openai_messages.insert(
        len(openai_messages) - 1,
        {"role": "user", "content": gen_doc_prompt(top_docs)}
    )

    logger.info(f"Openai messages: {openai_messages}")

    assistant_answer = openai_chat_complete(openai_messages)

    logger.info(f"Openai reply: {assistant_answer}")
    return assistant_answer
