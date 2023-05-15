# python-dotenv
from dotenv import load_dotenv
import os
# discord libraries
import hikari
import lightbulb
import miru
# miscellaneous
import logging

# uvloop for performance on UNIX systems
if os.name != "nt":
    import uvloop
    uvloop.install()

# initializing everything
load_dotenv()
logger = logging.getLogger('tttt.bot')
bot = lightbulb.BotApp(token=os.getenv('TOKEN'), prefix=os.getenv('PREFIX'), banner=None, intents=hikari.Intents.ALL_UNPRIVILEGED)
miru.install(bot)

# creating objects/connections
@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.logger = logger
    logger.info("Added logger to datastore")

bot.load_extensions_from("./extensions/", must_exist=True)

# running the bot
bot.run()