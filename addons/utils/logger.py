from datetime import date, datetime
from sys import _getframe
from asyncio import ensure_future
from discord import Embed, Color
from discord.errors import Forbidden
from addons.utils.formatting import escape


class Logger:

    def __init__(self, name, channel=None, *, stftime="%d/%m/%Y %H:%M"):
        self.name = name
        self.channel = channel
        self.strftime = stftime

    def write(self, content, type, function):
        time = datetime.now().strftime(self.strftime)
        with open("logs/{}.log".format(str(date.today())), "a") as file:
            file.write("[{time}] {type} {name} {function}: {content}\n".format(
                time=time, type=type, name=self.name, function=function, content=content))

    def send(self, content, type, function, color="#ffffff"):
        async def wrapper(self, content, type, function):
            emb = Embed(color=color)
            (emb.add_field(name="Type", value=type)
                .add_field(name="Name", value=escape(self.name))
                .add_field(name="Function", value=escape(function))
                .add_field(name="Message", value=escape(content), inline=True))
            try:
                await self.channel.send(embed=emb)
            except Forbidden:
                await self.channel.send("{type} {name} {function}: {content}\n".format(type=type, name=self.name, function=function, content=content))
        ensure_future(wrapper(self, content, type, function))

    def info(self, content):
        type = "INFO"
        function = _getframe(1).f_code.co_name
        self.write(content, type, function)
        if self.channel:
            self.send(content, type, function, Color.green())

    def warn(self, content):
        type = "WARNING"
        function = _getframe(1).f_code.co_name
        print(content)
        self.write(content, type, function)
        if self.channel:
            self.send(content, type, function, Color.red())
