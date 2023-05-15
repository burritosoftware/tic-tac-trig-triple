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
            match rows:
                case 0:
                    formattedBoard += "\n0️⃣"
                case 1:
                    formattedBoard += "\n1️⃣"
                case 2:
                    formattedBoard += "\n2️⃣"
                case 3:
                    formattedBoard += "\n3️⃣"
                case 4:
                    formattedBoard += "\n4️⃣"
                case 5:
                    formattedBoard += "\n5️⃣"
                case 6:
                    formattedBoard += "\n6️⃣"
                case 7:
                    formattedBoard += "\n7️⃣"
                case 8:
                    formattedBoard += "\n8️⃣"
            rows += 1
            for value in row:
                match value:
                    case "E":
                        formattedBoard += "⬛"
                    case "1":
                        formattedBoard += "🔷"
                    case "2":
                        formattedBoard += "🔶"
                    case "3":
                        formattedBoard += "♦️"
        return hikari.Embed(title="Game Session", color="8cb5b1", description=formattedBoard)
    
    def claimSpace(self, x, y, p):
        if self.array[x][y] != "E":
            return False
        self.array[x][y] = p
        return True

    def get_winner(self):
        for i in range(9):
            for j in range(9):
                if self.array[i][j] != "E":
                    if (j < 7 and self.array[i][j] == self.array[i][j + 1] == self.array[i][j + 2]) or \
                            (i < 7 and self.array[i][j] == self.array[i + 1][j] == self.array[i + 2][j]) or \
                            (i < 7 and j < 7 and self.array[i][j] == self.array[i + 1][j + 1] == self.array[i + 2][j + 2]) or \
                            (i < 7 and j > 1 and self.array[i][j] == self.array[i + 1][j - 1] == self.array[i + 2][j - 2]):
                        return self.array[i][j]
        return None

class TicTacModal(miru.Modal):
    yCoord = miru.TextInput(label="X Coordinate", required=True)
    xCoord = miru.TextInput(label="Y Coordinate", required=True)

    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.edit_response("Processing...")

class TicTacController(miru.View):
    @miru.button(label="Take a Turn", style=hikari.ButtonStyle.SUCCESS)
    async def takeTurn(self, button: miru.Button, ctx: miru.ViewContext):
        # if ctx.author.id is found inside the message that this button is attached to, or if the author's id is in the owner ids to override
        if str(ctx.author.id) in ctx.message.content or ctx.author.id in await ctx.bot.fetch_owner_ids():
            chooser = TicTacModal(title="Choose a tile to place!")
            num1 = random.randint(10, 100)
            num2 = random.randint(10, 100)
            mathQuestion = miru.TextInput(label=f"Solve this math problem: {num1} + {num2}", required=True)
            chooser.add_item(mathQuestion)
            await ctx.respond_with_modal(chooser)
            await chooser.wait()

            self.xCoord = chooser.xCoord.value
            self.yCoord = chooser.yCoord.value
            self.num1 = num1
            self.num2 = num2
            self.mathAnswer = chooser.values[mathQuestion]
            self.running = True
            self.stop()
            # Return a value that signals to the command to create a modal to get the player's input
        else:
            # Respond ephemerally to the user
            await ctx.respond("It's not your turn! Please wait for the other player.", flags=hikari.MessageFlag.EPHEMERAL)
    
    @miru.button(label="🗑️", style=hikari.ButtonStyle.DANGER)
    async def abort(self, button: miru.Button, ctx: miru.ViewContext):
        if "TTTT" + str(ctx.author.id) in ctx.message.content or ctx.author.id in await ctx.bot.fetch_owner_ids():
            self.running = False
            self.stop()
        else:
            await ctx.respond("You cannot abort a game that you didn't start!", flags=hikari.MessageFlag.EPHEMERAL)

@plugin.command
@lightbulb.option("player3", "Third player", type=hikari.User)
@lightbulb.option("player2", "Second player", type=hikari.User)
@lightbulb.command("start", description="Start a new tic-tac-trig-triple game between 2 other players!")
@lightbulb.implements(lightbulb.SlashCommand)
async def start(ctx: lightbulb.Context) -> None:
    # Each of our players
    player1 = ctx.user
    player2 = ctx.options.player2
    player3 = ctx.options.player3
    
    # Preventing an invalid set of palyers
    if player1 == player2 or player2 == player3 or player1 == player3:
        await ctx.respond("You cannot play against yourself or have duplicate players! Please try again.")
        return

    board = TicTacBoard()
    await ctx.respond("Loading...")

    # Disabled button controller to put when the player shouldn't be able to take a turn
    disabledcontroller = TicTacController()
    for item in disabledcontroller.children:
        item.disabled = True

    async def advance(player):
        controller = TicTacController()

        message = await ctx.edit_last_response(content=f"It's <@{player.id}>'s turn!\n> **Players:** 👑 *{player1.username}#{player1.discriminator}*, {player2.username}#{player2.discriminator}, {player3.username}#{player3.discriminator}\n> **Game ID:** TTTT{player1.id}", embed=board.formatBoard(), components=controller)
        await controller.start(message)
        await controller.wait()

        if controller.running == False:
            await ctx.edit_last_response(content=f"Game was aborted by the game starter: <@{player1.id}>", components=disabledcontroller)
            return False

        try:
            if int(controller.xCoord) > 8 or int(controller.xCoord) < 0 or int(controller.yCoord) > 8 or int(controller.yCoord) < 0:
                await ctx.edit_last_response(content=f"<@{player.id}> entered an invalid coordinate! Advancing in 3 seconds...", components=disabledcontroller)
                await asyncio.sleep(3)
            else:
                if str(controller.num1 + controller.num2) == controller.mathAnswer:
                    playerId = 0
                    if player == player1:
                        playerId = 1
                    elif player == player2:
                        playerId = 2
                    elif player == player3:
                        playerId = 3
                    
                    spaceGiven = board.claimSpace(int(controller.xCoord), int(controller.yCoord), str(playerId))
                    if spaceGiven == False:
                        await ctx.edit_last_response(content=f"<@{player.id}> tried to claim an already claimed tile! Advancing in 3 seconds...", components=disabledcontroller)
                        await asyncio.sleep(3)
                else:
                    await ctx.edit_last_response(content=f"<@{player.id}> got the math problem answer wrong! {controller.num1} + {controller.num2} = {controller.num1 + controller.num2}. Advancing in 3 seconds...", components=disabledcontroller)
                    await asyncio.sleep(3)
        except ValueError:
            await ctx.edit_last_response(content=f"<@{player.id}> made a mistake entering their answer! Advancing in 3 seconds...", components=disabledcontroller)
            await asyncio.sleep(3)

    # Main game loop, if the game is aborted return
    while board.get_winner() == None:
        if board.get_winner() == None:
            if await advance(player1) == False:
                return
        if board.get_winner() == None:
            if await advance(player2) == False:
                return
        if board.get_winner() == None:
            if await advance(player3) == False:
                return

    winner = player1
    match board.get_winner():
        case "1":
            winner = player1
        case "2":
            winner = player2
        case "3":
            winner = player3

    await ctx.edit_last_response(content=f"Congratulations, <@{winner.id}>! You won!", embed=board.formatBoard(), components=disabledcontroller)
    return
        

def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)