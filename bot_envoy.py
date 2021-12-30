from discord import Intents, utils
from discord.ext.commands import Bot
import asyncio
from os import environ
from random import choice
from datetime import datetime
import hoi_draft as hoi

bot_allow_channel=environ['BOT_CHANNEL']

cmds = [
    'ayuda',
    'ruleta',
    'ruleta majors',
    'ruleta minors'
]


class Envoy(Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # create the background task and run it in the background
    # self.bg_task = self.loop.create_task(self.spam())
    self.last_msg = None

  async def spam(self):
    await self.wait_until_ready()
    bot_channel = utils.get(self.get_all_channels(), name=bot_allow_channel)
    while not self.is_closed():
      if bot_channel:
        await asyncio.sleep(600)
        await bot_channel.send(f'still allive - {datetime.now()}')

  async def on_ready(self):
    print(f'{self.user} ready, sir!')
    bot_channel = utils.get(self.get_all_channels(), name=bot_allow_channel)
    if bot_channel:
      await bot_channel.send(choice(bot_ready_msg))


intents = Intents.default()
bot = Diplomat(command_prefix='hoi ', case_insensitive=True, intents=intents)

@bot.command()
async def ayuda(ctx):
  comandos = ', '.join(cmds)
  await ctx.send(f'Comandos disponibles: {comandos}')


@bot.command()
async def modo(ctx):
  await ctx.send(f'Modo: {choice(modos)}')

@bot.group()
async def ruleta(ctx):
    if not ctx.invoked_subcommand:
        await ctx.send('¿Qué tipo de ruleta? \n Reiniciando ruleta...')
        # guardar?
        hoi.regen_pool()

@ruleta.group()
async def ban(ctx):
    pritn(ctx.message)

@ruleta.group()
async def majors(ctx):
    await ctx.send('Tu pais sera', hoi.get_major())

@ruleta.group()
async def minors(ctx):
    await ctx.send('Tu pais sera', hoi.get_minor())
