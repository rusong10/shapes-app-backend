from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import UserShape
from .serializers import UserShapeSerializer
from .consumers import SHAPES_GROUP_NAME

@receiver(post_save, sender=UserShape)
def announce_shape_change(sender, instance, created, **kwargs):
    """
    Signal handler for when a UserShape is saved (created or updated).
    """

    channel_layer = get_channel_layer()
    action = "created" if created else "updated"
    shape_data = UserShapeSerializer(instance).data 

    message_data = {
        'action': action,
        'shape': shape_data,
    }

    print(f"Signal: Shape {action} - ID: {instance.id}. Broadcasting to group {SHAPES_GROUP_NAME}")

    async_to_sync(channel_layer.group_send)(
        SHAPES_GROUP_NAME,
        {
            "type": "shapes.update.message",
            "data": message_data,
        }
    )

@receiver(post_delete, sender=UserShape)
def announce_shape_delete(sender, instance, **kwargs):
    """
    Signal handler for when a UserShape is deleted.
    """
    channel_layer = get_channel_layer()

    message_data = {
        'action': 'deleted',
        'shape_id': instance.id, # Send the ID of the deleted shape
    }

    print(f"Signal: Shape deleted - ID: {instance.id}. Broadcasting to group {SHAPES_GROUP_NAME}")

    async_to_sync(channel_layer.group_send)(
        SHAPES_GROUP_NAME,
        {
            "type": "shapes.update.message",
            "data": message_data,
        }
    )
