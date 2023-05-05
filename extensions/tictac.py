import lightbulb
import hikari
import miru

plugin = lightbulb.Plugin("Tic Tac Trig Triple")

class TicTacBoard:
    # E = empty space
    # X = Player 1 Claim
    # Y = Player 2 Claim
    # Z = Player 3 Claim
    def __init__(self):
        self.array = [ ["E" for x in range (9)] for y in range (9)]

    def formatBoard(self):
        formattedBoard = ""
        for row in self.array:
            for value in row:
                if value == "E":
                    formattedBoard += "⬛"
                elif value == "X":
                    formattedBoard += "🔷"
                elif value == "Y":
                    formattedBoard += "🔶"
                elif value == "Z":
                    formattedBoard += "♦️"
            formattedBoard += "\n"
        return hikari.Embed(title="Game Board", description=formattedBoard)
    
    def claimSpace(self, x, y, p):
        if self.array[x][y] != "E":
            return False
        self.array[x][y] = p
        return True

@plugin.command
@lightbulb.command("start", description="Start a new tic-tac-trig-triple game between 2 other players!")
@lightbulb.implements(lightbulb.SlashCommand)
async def start(ctx: lightbulb.Context) -> None:
    board = TicTacBoard();
    await ctx.respond(embed=board.formatBoard())
    board.claimSpace(2,3,"X")
    board.claimSpace(3,3,"Y")
    board.claimSpace(4,3,"Z")
    await ctx.respond(embed=board.formatBoard())

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)