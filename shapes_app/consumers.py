import json
from channels.generic.websocket import AsyncWebsocketConsumer

SHAPES_GROUP_NAME = "shapes_updates" # Name of the group to broadcast to

class ShapeConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
        Called when the websocket is trying to connect.
        """

        self.group_name = SHAPES_GROUP_NAME

        # Join shapes group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"WebSocket connected: {self.channel_name}, User: {self.scope.get('user', 'Anonymous')}")

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Remove this channel from the 'shapes_updates' group
        await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
        )
        print(f"WebSocket disconnected: {self.channel_name} from group {self.group_name}")

    async def shapes_update_message(self, event):
        """
        Handler for messages sent to the shapes_updates group.
        This method name must match the 'type' in the group_send call,
        with '.' replaced by '_'.
        """
        print(f"Received event: {event}")
        message_data = event['data'] # The data sent from the signal handler

        # Send message data to WebSocket client
        await self.send(text_data=json.dumps(message_data))
        print(f"Sent update to {self.channel_name}: {message_data}")
