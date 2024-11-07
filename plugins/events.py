import json

from khl import Bot, Event, EventTypes

def initEvents(bot: Bot):
    @bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
    async def button_click_event(bot: Bot, e: Event):
        value: dict = json.loads(e.body.get('value', '{"event": "", "args": ()}'))
        # Code Here.
        ...
        # Code Here.
