import asyncio
import loc_strings as loc
import hoi_draft as hoi
from os import environ
from random import choice
from datetime import datetime
from discord import Intents, utils
from discord.ext.commands import Bot

bot_allow_channel=environ['BOT_CHANNEL']

cmds = [
  f'ayuda',
  f'ruleta reiniciar: {loc.HELP_ROULETTE_RESET}',
  f'ruleta majors: {loc.HELP_ROULETTE_MAJ}',
  f'ruleta minors: {loc.HELP_ROULETTE_MIN}',
  f'ruleta ban: {loc.HELP_ROULETTE_BAN}',
  f'ruleta commies: {loc.HELP_ROULETTE_COMMIES}',
  f'ruleta fascis: {loc.HELP_ROULETTE_FASCIS}',
  f'ruleta demo: {loc.HELP_ROULETTE_DEMO}',
  f'ruleta nonaligned: {loc.HELP_ROULETTE_NONA}',
]

class Envoy(Bot):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # create the background task and run it in the background
    # self.bg_task = self.loop.create_task(self.spam())
    hoi.regen_pool()

  # async def spam(self):
  #  await self.wait_until_ready()
  #  bot_channel = utils.get(self.get_all_channels(), name=bot_allow_channel)
  #  while not self.is_closed():
  #    if bot_channel:
  #      await asyncio.sleep(600)
  #      await bot_channel.send(f'{BOT_READY} - {datetime.now()}')

  async def on_ready(self):
    bot_channel = utils.get(self.get_all_channels(), name=bot_allow_channel)
    if bot_channel:
      await bot_channel.send((f'{self.user} {loc.BOT_READY}'))
      print(f'{self.user} {loc.BOT_READY}')

intents = Intents.default()
bot = Envoy(command_prefix='hoi ', case_insensitive=True, intents=intents)

@bot.command()
async def ayuda(ctx):
  comandos = '\n'.join(cmds)
  await ctx.send(f'{loc.BOT_HELP} {comandos}')

@bot.group()
async def ruleta(ctx):
  if not ctx.invoked_subcommand:
    pass

@ruleta.group()
async def ban(ctx):
  # print(ctx.message.content)
  # remove command 
  target = ctx.message.content.replace('hoi ruleta ban ', '')
  if hoi.ban(target):
    await ctx.send(f'{target} removido del sorteo')
  else:
    await ctx.send(f'No se pudo encontrar el pais {target}')

@ruleta.group()
async def reiniciar(ctx):
  hoi.regen_pool()
  await ctx.send(loc.BOT_ROULETTE_RESET)

@ruleta.group()
async def majors(ctx):
  await ctx.send(f'{loc.BOT_ROULETTE_RESULT} {hoi.get_major()}')

@ruleta.group()
async def minors(ctx):
  await ctx.send(f'{loc.BOT_ROULETTE_RESULT} {hoi.get_minor()}')

@ruleta.group()
async def demo(ctx):
  await ctx.send(f'{loc.BOT_ROULETTE_RESULT} {hoi.get_democracies()}')

@ruleta.group()
async def commies(ctx):
  await ctx.send(f'{loc.BOT_ROULETTE_RESULT} {hoi.get_commies()}')

@ruleta.group()
async def fascis(ctx):
  await ctx.send(f'{loc.BOT_ROULETTE_RESULT} {hoi.get_fascis()}')

@ruleta.group()
async def nonaligned(ctx):
  await ctx.send(f'{loc.BOT_ROULETTE_RESULT} {hoi.get_nonaligned()}')

