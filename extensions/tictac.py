import lightbulb
import hikari
import miru

plugin = lightbulb.Plugin("Tic Tac Trig Triple")

class TicTacBoard:
    rows = 9
    cols = 9
    array = [ ["E" for x in range (cols)] for y in range (rows)]

    def formatBoard(self):
        formattedBoard = ""
        for row in array:
            for value in row:
                if value == "E":
                    formattedBoard += "⬛"
            formattedBoard += "\n"
        return hikari.Embed(title="Game Board", description=formattedBoard)

@plugin.command
@lightbulb.command("start", description="Start a new tic-tac-trig-triple game between 2 other players!")
@lightbulb.implements(lightbulb.SlashCommand)
async def start(ctx: lightbulb.Context) -> None:
    board = TicTacBoard();
    ctx.respond("")

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)