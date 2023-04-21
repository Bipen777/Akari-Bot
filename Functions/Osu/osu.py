import pygsheets
import discord
import datetime
import random
from datetime import timezone
from discord import Interaction
from discord.ui import Button, View
from discord.ext import commands, tasks

sheet_client = pygsheets.authorize(service_account_file="Google Sheets JSON here")

class MatchView(View):
    def __init__(self, ctx, msg: discord.Embed, mods: list, team1: list, team2: list):
        super().__init__(timeout=None) 
        self.add_item(Button(label="Refsheet", url="Sheet Link Here"))
        self.round = 1
        self.ctx = ctx
        self.msg = msg
        self.fields = [mods,team1,team2]
        self.confirm = False

    @discord.ui.button(custom_id="prev", label="Prev", style=discord.ButtonStyle.green, emoji="<:din:977356069833703474>", disabled=True)
    async def prev_callback(self,interaction: Interaction,button: Button):
        self.round-=1
        self.confirm = False if self.confirm == True else False
        self.msg.colour = discord.Color.green()
        end = [i for i in self.children if i.custom_id == "end"][0]
        end.label = "End Match"
        button.disabled = False if self.round > 1 else True
        for i in range(len(self.msg.fields)):
            self.fields[i] = self.fields[i][-1:] + self.fields[i][:-1]
            self.msg.set_field_at(i,name=self.msg.fields[i].name, value=self.fields[i])
        await interaction.response.edit_message(content="Round: "+str(self.round),embed=self.msg,view=self)

    @discord.ui.button(custom_id="next", label="Next", style=discord.ButtonStyle.green, emoji="<:hai:679557663469731849>")
    async def next_callback(self,interaction: Interaction,button: Button):
        self.round+=1
        self.confirm = False if self.confirm == True else False
        self.msg.colour = discord.Color.green()
        end = [i for i in self.children if i.custom_id == "end"][0]
        end.label = "End Match"
        prev = [i for i in self.children if i.custom_id == "prev"][0]
        prev.disabled = False
        for i in range(len(self.msg.fields)):
            self.fields[i] = self.fields[i][1:] + self.fields[i][:1]
            self.msg.set_field_at(i,name=self.msg.fields[i].name, value=self.fields[i])
        await interaction.response.edit_message(content="Round: "+str(self.round),embed=self.msg,view=self)

    @discord.ui.button(custom_id="skip1", label="Skip Team 1", style=discord.ButtonStyle.primary, row=1)
    async def skip1_callback(self, interaction: Interaction, button: Button):
        self.confirm = False if self.confirm == True else False
        self.msg.colour = discord.Color.green()
        end = [i for i in self.children if i.custom_id == "end"][0]
        end.label = "End Match"
        self.fields[1] = self.fields[1][1:] + self.fields[1][:1]
        self.msg.set_field_at(1,name=self.msg.fields[1].name, value=self.fields[1])
        await interaction.response.edit_message(embed=self.msg, view=self)

    @discord.ui.button(custom_id="skip2", label="Skip Team 2", style=discord.ButtonStyle.primary, row=1)
    async def skip2_callback(self, interaction: Interaction, button: Button):
        self.confirm = False if self.confirm == True else False
        self.msg.colour = discord.Color.green()
        end = [i for i in self.children if i.custom_id == "end"][0]
        end.label = "End Match"
        self.fields[2] = self.fields[2][1:] + self.fields[2][:1]
        self.msg.set_field_at(2,name=self.msg.fields[2].name, value=self.fields[2])
        await interaction.response.edit_message(embed=self.msg, view=self)

    @discord.ui.button(custom_id="end", label="End Match", style=discord.ButtonStyle.red, row=2)
    async def end_callback(self, interaction: Interaction, button: Button):
        if self.confirm == True:
            self.msg.colour = discord.Color.red()
            await interaction.response.edit_message(content="Match Over", embed=self.msg, view=None)
        else:
            self.msg.colour = discord.Color.orange()
            button.label = "Are you sure?"
            self.confirm = True
            await interaction.response.edit_message(embed=self.msg, view=self)

    async def interaction_check(self, interaction: Interaction) -> bool:
        if interaction.user.name != self.ctx.author.name:
            await interaction.response.send_message("You're not the ref of this match.", ephemeral=True)
            return False
        else:
            return True

    async def on_error(self, interaction: Interaction, error: Exception, item) -> None:
        self.stop()
        await interaction.response.send_message("Whoopse : " + str(error))

class Osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def test(self, ctx, data):
        sheet = sheet_client.open("Test Sheet")
        tab = sheet.worksheet("title", "Sheet1")

        # i = 1
        # while not tab.cell("A"+str(i)) == "<Cell A" + str(i) + " ''>" and i < 1000:
        #     i+=1
        # if i < 1000:
        tab.cell("A1").value = data

        await ctx.send("" + str(data) + " was put into A1")

    @commands.command()
    async def match(self, ctx, ID):
# init the embed modules
        mods  = ["NM","HD","HR","DT","FM"]
        team1 = ['1','2','3','4']
        team2 = ['1','2','3','4']
        team1n = 'asdf'
        team2n = 'asdf2'
        f1, f2 = (False,False)
# init referances for sheets
        admin_sheet = sheet_client.open("RNG Fest Admin")
        ref_sheet   = sheet_client.open("RNG Fest Ref Sheet")
        team_tab    = admin_sheet.worksheet("title", "FilterTeams")
        bracket_tab = ref_sheet.worksheet("title", "Bracket Schedule")
# find team names and teammate names    
        IDlist = bracket_tab.range('C2:C190')  
        IDpos = 2
        for i in IDlist:
            if i[0].value == ID:
                IDpos = i[0].row
        team1n = bracket_tab.cell("J"+str(int(IDpos))).value
        team2n = bracket_tab.cell("K"+str(int(IDpos))).value
        teamlist = team_tab.range('D2:D120')
        count = 2
        for i in teamlist:
            si = str(count)
            if f1 and f2 == True:
                break
            if i[0].value == team1n:
                f1 = True
                team1[0] = team_tab.cell("H"+si).value
                team1[1] = team_tab.cell("I"+si).value
                team1[2] = team_tab.cell("J"+si).value
                team1[3] = team_tab.cell("K"+si).value
            if i[0].value == team2n:
                f2 = True
                team2[0] = team_tab.cell("H"+si).value
                team2[1] = team_tab.cell("I"+si).value
                team2[2] = team_tab.cell("J"+si).value
                team2[3] = team_tab.cell("K"+si).value
            count += 1
        if len(team1[3]) == 0:
            team1.pop()
        if len(team2[3]) == 0:
            team2.pop()

# randomize the modules
        mods = random.sample(mods,5)
        if len(team1) == 4:
            team1 = random.sample(team1,4)
        else:
            team1 = random.sample(team1,3)
        if len(team2) == 4:
            team2 = random.sample(team2,4)
        else:
            team2 = random.sample(team2,3)
# generate the return
        msg = discord.Embed(
            title= team1n + " vs " + team2n,
            description="Copy and paste this to the mp lobby.",
            colour=discord.Colour.green()
        )
        msg.add_field(name="Modpool Order: ",value=mods)
        msg.add_field(name=team1n +': ',value=team1)
        msg.add_field(name=team2n +': ',value=team2)
        btns = MatchView(ctx, msg, mods, team1, team2)

        await ctx.send(content="Round: 1",embed=msg, view=btns)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def schon(self, ctx):
        self.check_schedule.start(ctx)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def schoff(self, ctx):
        self.check_schedule.cancel()

    @tasks.loop(minutes=15)
    async def check_schedule(self, ctx):
        sheet = sheet_client.open("Test Sheet")
        tab = sheet.worksheet("title","Bracket Schedule")

        dt = datetime.datetime.now(timezone.utc)
        strdt = dt.strftime("%#m/%#d %#H:%M")

        msg = discord.Embed(
            title="Matches Today!",
            description=dt.strftime("Matches on: %a, %b %#d"),
            colour=discord.Colour.orange()
        )
        for i in range(2,97):
            si = str(i)
            tdt = str(tab.cell("D"+si).value + " " + tab.cell("E"+si).value)
            if tdt == ' ':
                break
            mdt = datetime.datetime.strptime(tdt, "(%a) %b %d %H:%M")
            if mdt.month == dt.month and mdt.day == dt.day:
                msg.add_field(name=str(tab.cell("C"+si).value), value=str(tab.cell("J"+si).value + " vs " + tab.cell("K"+si).value + ": " + tdt), inline=True)
        await ctx.send(embed=msg)
    
async def setup(bot):
    await bot.add_cog(Osu(bot))