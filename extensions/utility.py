import lightbulb

plugin = lightbulb.Plugin("Utility")

@plugin.command
@lightbulb.command("ping", description="Gets the bot's latency", ephemeral=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond(f":ping_pong: **Pong!** Latency: {ctx.bot.heartbeat_latency*1000:.2f}ms")
def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)