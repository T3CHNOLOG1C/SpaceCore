from datetime import date, datetime
from sys import _getframe
from asyncio import ensure_future
from discord import Embed


class Logger:

    def __init__(self, name, channel=None, *, stftime="%d/%m/%Y %H:%M", writeformat="[{time}] {type} {name} {function}: {content}\n"):
        self.name = name
        self.channel = channel
        self.strftime = stftime
        self.writeformat = writeformat

    def write(self, content, type, function):
        with open("logs/{}.log".format(str(date.today())), "a") as file:
            file.write()

    def send(self, content, type, function):
        async def wrapper(self, content, type, function):
            emb = Embed()
            emb.add_field(name="Name", value=self.name)
            emb.add_field(name="Type", value=type)
            emb.add_field(name="Function", value=function)
            emb.add_field(name="Message", value=content)
            await self.channel.send(embed=emb)
        ensure_future(wrapper(self, content, type, function))

    def info(self, content):
        type = "INFO"
        function = _getframe(1).f_code.co_name
        time = datetime.now().strftime(self.strftime)
        content = self.writeformat.format(
            time=time, type=type, name=self.name, function=function, content=content)

        self.write(content, type, function)
        if self.channel:
            self.send(content, type, function)

    def warn(self, content):
        type = "WARNING"
        function = _getframe(1).f_code.co_name
        time = datetime.now().strftime(self.strftime)
        content = self.writeformat.format(
            time=time, type=type, name=self.name, function=function, content=content)

        print(content)
        self.write(content, type, function)
        if self.channel:
            self.send(content, type, function)
