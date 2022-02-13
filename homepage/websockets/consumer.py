from channels.generic.websocket import AsyncJsonWebsocketConsumer


class PaymentSuccessfullMessage(AsyncJsonWebsocketConsumer):
    async def connect(self):
         await self.channel_layer.group_add('mpesa_successful',self.channel_name)
         await self.accept()

    async def disconnect(self,code):
         await self.channel_layer.group_discard('mpesa_successful',self.channel_name)

    async def send_footballl_twowayp(self,event):
        text_message = event['text']
        await self.send_json(text_message)











