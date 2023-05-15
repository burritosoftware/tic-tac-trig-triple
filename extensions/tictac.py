import lightbulb
import hikari
import miru
import random
import asyncio

plugin = lightbulb.Plugin("Tic Tac Trig Triple")

class TicTacBoard:
    # E = empty space
    # X = Player 1 Claim
    # Y = Player 2 Claim
    # Z = Player 3 Claim
    def __init__(self):
        self.array = [ ["E" for x in range (9)] for y in range (9)]

    def formatBoard(self):
        formattedBoard = "⬛0️⃣1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣"
        rows = 0
        for row in self.array:
            if rows == 0:
                formattedBoard += "\n0️⃣"
            elif rows == 1:
                formattedBoard += "\n1️⃣"
            elif rows == 2:
                formattedBoard += "\n2️⃣"
            elif rows == 3:
                formattedBoard += "\n3️⃣"
            elif rows == 4:
                formattedBoard += "\n4️⃣"
            elif rows == 5:
                formattedBoard += "\n5️⃣"
            elif rows == 6:
                formattedBoard += "\n6️⃣"
            elif rows == 7:
                formattedBoard += "\n7️⃣"
            elif rows == 8:
                formattedBoard += "\n8️⃣"
            rows += 1
            for value in row:
                if value == "E":
                    formattedBoard += "⬛"
                elif value == "1":
                    formattedBoard += "🔷"
                elif value == "2":
                    formattedBoard += "🔶"
                elif value == "3":
                    formattedBoard += "♦️"
        return hikari.Embed(title="Game Board", description=formattedBoard)
    
    def claimSpace(self, x, y, p):
        if self.array[x][y] != "E":
            return False
        self.array[x][y] = p
        return True

class TicTacModal(miru.Modal):
    yCoord = miru.TextInput(label="X Coordinate", required=True)
    xCoord = miru.TextInput(label="Y Coordinate", required=True)
    num1 = random.randint(10, 100)
    num2 = random.randint(10, 100)
    mathProblem = miru.TextInput(label=f"Solve this math problem: {num1} + {num2}", required=True)

    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.edit_response("Processing...")

class TicTacController(miru.View):
    @miru.button(label="Take a Turn", style=hikari.ButtonStyle.SUCCESS)
    async def takeTurn(self, button: miru.Button, ctx: miru.ViewContext):
        chooser = TicTacModal(title="Choose a tile!")
        await ctx.respond_with_modal(chooser)
        await chooser.wait()
        # TODO: figure out how to get values from chooser.values
        self.xCoord = chooser.xCoord.value
        self.yCoord = chooser.yCoord.value
        self.num1 = chooser.num1
        self.num2 = chooser.num2
        self.mathProblem = chooser.mathProblem.value
        self.stop()
        # Return a value that signals to the command to create a modal to get the player's input

@plugin.command
@lightbulb.option("player3", "Third player", type=hikari.User)
@lightbulb.option("player2", "Second player", type=hikari.User)
@lightbulb.command("start", description="Start a new tic-tac-trig-triple game between 2 other players!")
@lightbulb.implements(lightbulb.SlashCommand)
async def start(ctx: lightbulb.Context) -> None:
    player1 = ctx.user
    player2 = ctx.options.player2
    player3 = ctx.options.player3
    board = TicTacBoard()
    message = await ctx.respond("Loading...")

    async def advance(player):
        controller = TicTacController()
        message = await ctx.edit_last_response(content=f"It's <@{player.id}>'s turn!", embed=board.formatBoard(), components=controller)
        await controller.start(message)
        await controller.wait()

        if str(controller.num1 + controller.num2) == controller.mathProblem:
            playerId = 0
            if player == player1:
                playerId = 1
            elif player == player2:
                playerId = 2
            elif player == player3:
                playerId = 3
            board.claimSpace(int(controller.xCoord), int(controller.yCoord), str(playerId))
        else:
            await ctx.edit_last_response(content=f"<@{player.id}> got the math problem answer wrong! Advancing in 5 seconds...")
            await asyncio.sleep(5)

    while True:
        await advance(player1)
        await advance(player2)
        await advance(player3)
        

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)