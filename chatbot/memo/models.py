import logging

from django.db import models
from django.utils import timezone


class ChatConversation(models.Model):
    conversation_id = models.CharField(max_length=50, null=False, default="")
    bot_id = models.CharField(max_length=100, null=False)
    user_id = models.CharField(max_length=100, null=False)
    message = models.TextField()
    is_request = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.conversation_id


def convert_conversation_to_openai_messages(conversation_id):
    user_conversations = ChatConversation.objects.filter(conversation_id=conversation_id).order_by('created_at')
    conversation_list = [
        {
            "role": "system",
            "content": "You are an amazing virtual assistant"
        }
    ]

    for conversation in user_conversations:
        role = "assistant" if not conversation.is_request else "user"
        content = str(conversation.message)
        conversation_list.append({"role": role, "content": content})

    logging.info(f"Create conversation to {conversation_list}")

    return conversation_list


class Document(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('title', 'content')

    def __str__(self):
        return self.title
