import json
import logging

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Document
from .brain import get_embedding
from .vectorize import add_vector
from .configs import DEFAULT_COLLECTION_NAME

logger = logging.getLogger(__name__)


def add_doc_to_vector_db(instance):
    if instance.title:
        vector = get_embedding(instance.title)
        logger.info(f"Embedding {instance.title} to vector")
        add_vector(
            DEFAULT_COLLECTION_NAME,
            {
                instance.id: {
                    "vector": vector,
                    "payload": {
                        "title": instance.title,
                        "content": instance.content
                    }
                }
            }
        )
    else:
        logger.error("Title and content is null")


@receiver(post_save, sender=Document)
def create_document_to_vector_db(sender, instance, created, **kwargs):
    logger.info("create_document_to_vector_db")
    if created:
        add_doc_to_vector_db(instance)


@receiver(post_save, sender=Document)
def update_document_to_vector_db(sender, instance, **kwargs):
    logger.info("update_document_to_vector_db")
    add_doc_to_vector_db(instance)
