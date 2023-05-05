# python-dotenv
from dotenv import load_dotenv
import os
# discord libraries
import hikari
import lightbulb
import miru
# miscellaneous
import aiohttp
import logging
import dataset

# uvloop for performance on UNIX systems
if os.name != "nt":
    import uvloop
    uvloop.install()

# initializing everything
load_dotenv()
logger = logging.getLogger('tttt.bot')
bot = lightbulb.BotApp(token=os.getenv('TOKEN'), prefix=os.getenv('PREFIX'), banner=None, default_enabled_guilds=(1104130814255566899), intents=hikari.Intents.ALL_UNPRIVILEGED)
miru.install(bot)

# creating objects/connections
@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()
    logger.info("Created aiohttp.ClientSession")
    bot.d.logger = logger
    logger.info("Added logger to datastore")
    bot.d.db = dataset.connect(os.getenv('DATABASE'), engine_kwargs=dict(connect_args={'check_same_thread': False}))
    logger.info(f"Connected to database {os.getenv('DATABASE')}")

# disposing objects/connections
@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    bot.d.db.close()
    logger.info("Closed database connection")
    # Close the ClientSession
    await bot.d.aio_session.close()
    logger.info("Closed aiohttp.ClientSession")

bot.load_extensions_from("./extensions/", must_exist=True)

# running the bot
bot.run()