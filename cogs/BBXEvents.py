import discord
from discord.ext import commands
import asyncio
import random
from asyncio import sleep, TimerHandle
import discord.user
from discord.utils import get
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from libneko import pag


"""__________________Google Sheets__________________"""
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "creds2.json", scope)

gclient = gspread.authorize(creds)

sheet = gclient.open("BBXINT_JUDGING").worksheet(
    'HOST')  # Open the spreadhseet
sheet2 = gclient.open("BBXINT_JUDGING").worksheet(
    'JUDGE 1')  # Open the spreadhseet
sheet3 = gclient.open("BBXINT_JUDGING").worksheet(
    'JUDGE 2')  # Open the spreadhseet
sheet4 = gclient.open("BBXINT_JUDGING").worksheet(
    'JUDGE 3')  # Open the spreadhseet
sheet5 = gclient.open("BBXINT_JUDGING").worksheet(
    'JUDGE 4')  # Open the spreadhseet\
sheet6 = gclient.open("BBXINT_JUDGING").worksheet(
    'JUDGE 5')  # Open the spreadhseet
sheet7 = gclient.open("BBXINT_JUDGING").worksheet(
    'Event: Top 16')  # Open the spreadhseet
sheet8 = gclient.open("BBXINT_JUDGING").worksheet(
    'Event: Top 8')  # Open the spreadhseet
sheet9 = gclient.open("BBXINT_JUDGING").worksheet(
    'Results')  # Open the spreadhseet
sheet10 = gclient.open("BBXINT_JUDGING").worksheet(
    'RANKCALC')  # Open the spreadhseet
sheet11 = gclient.open("BBXINT_JUDGING").worksheet(
    'NameID')  # Open the spreadhseet

data = sheet.get_all_records()  # Get a list of all records

"""_______________________Queue System Start_______________________"""

parts = {}
que = {}
locked = False
partnum = []
hasjusges = False


class EventQueue(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    """_____________________EVENT START________________________"""

    @commands.command()
    async def judges(self, ctx, j1: discord.Member, j2: discord.Member, j3: discord.Member):
        j1name = j1.display_name
        j2name = j2.display_name
        j3name = j3.display_name
        if j1name != "'(J)" or "(J)":
            await j1.edit(nick="'(J) " + j1name)
        role = discord.utils.get(
            j1.guild.roles, name="BBXINT Daily Judge")
        await discord.Member.add_roles(j1, role)
        await discord.Member.add_roles(j2, role)
        await discord.Member.add_roles(j3, role)
        embed1 = discord.Embed(
            title=(f"Yo {j1name}"), description=("Here are the **Judging Sheets** for Today's **Event** | You are **JUDGE 1**" + '\n' + "https://docs.google.com/spreadsheets/d/1FAIk6R9Rr12X-DyWlH3Z7vBUV8Ij74qGyTF4n86a66o/edit?usp=sharing"), color=0x5473de)
        embed1.set_author(
            name="BEATBOX INTERNATIONAL", url="https://www.beatboxinternational.com", icon_url="https://lh3.googleusercontent.com/a-/AOh14GiBlYNVkzQLbkdzK-prRDKGmfy2INbA9n3Og0A-Bg=s88")
        await j1.send(embed=embed1)
        sheet.update_cell(3, 7, j1name)
        embed2 = discord.Embed(
            title=(f"Yo {j2name}"), description=("Here are the **Judging Sheets** for **Today's Event** | You are **JUDGE 2**" + '\n' + "https://docs.google.com/spreadsheets/d/1FAIk6R9Rr12X-DyWlH3Z7vBUV8Ij74qGyTF4n86a66o/edit?usp=sharing"), color=0x5473de)
        embed2.set_author(
            name="BEATBOX INTERNATIONAL", url="https://www.beatboxinternational.com", icon_url="https://lh3.googleusercontent.com/a-/AOh14GiBlYNVkzQLbkdzK-prRDKGmfy2INbA9n3Og0A-Bg=s88")
        await j2.send(embed=embed2)
        sheet.update_cell(6, 7, j2name)
        embed3 = discord.Embed(
            title=(f"Yo {j3name}"), description=("Here are the **Judging Sheets** for **Today's Event** | You are **JUDGE 3**" + '\n' + "https://docs.google.com/spreadsheets/d/1FAIk6R9Rr12X-DyWlH3Z7vBUV8Ij74qGyTF4n86a66o/edit?usp=sharing"), color=0x5473de)
        embed3.set_author(
            name="BEATBOX INTERNATIONAL", url="https://www.beatboxinternational.com", icon_url="https://lh3.googleusercontent.com/a-/AOh14GiBlYNVkzQLbkdzK-prRDKGmfy2INbA9n3Og0A-Bg=s88")
        await j3.send(embed=embed2)
        sheet.update_cell(9, 7, j3name)

    """__________________Join & Leave__________________"""

    @commands.command()
    async def join(self, ctx):
        if locked == False:
            global parts
            global que
            if discord.utils.get(ctx.message.author.roles, name="Participant"):

                print('in queue')
                embed = discord.Embed(
                    title=("You are already in the Queue! If it doesn't show you in the Queue," + '\n' + "then !leave & !join again!"), color=0xf55742)
                await ctx.send(embed=embed)

            else:
                member = ctx.author
                role = discord.utils.get(
                    member.guild.roles, name="Participant")
                await discord.Member.add_roles(member, role)
                print('not in queue')
                part = ctx.message.author.display_name
                nick = ctx.message.author.display_name
                userid = ctx.message.author.id
                namecode = [nick, str(userid), "True"]
                if sheet11.findall(nick):
                    cell = sheet11.find(nick)
                    row_number = cell.row
                    print(cell.row)
                    workbook2_row = 'C'+str(row_number)
                    print(workbook2_row)
                    sheet11.update_acell(workbook2_row, ('TRUE'))
                else:
                    sheet11.append_row(namecode, value_input_option='USER_ENTERED',
                                       insert_data_option='INSERT_ROWS', table_range='A1:C1')

                parts = part

                if id in que:
                    que[id].append(part)
                else:
                    que[id] = [part]

                embed = discord.Embed(
                    title=(part + ' has been Added to the Queue'), color=0xaaf542)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title=('The Queue is Locked!'), color=0xf55742)
            await ctx.send(embed=embed)

    @commands.command()
    async def leave(self, ctx):
        global parts
        member = ctx.author
        nick = ctx.message.author.display_name
        print(nick)
        role = discord.utils.get(member.guild.roles, name="Participant")
        await discord.Member.remove_roles(member, role)
        x = ctx.message.author.display_name
        print('Position', x)
        embed = discord.Embed(
            title=(ctx.message.author.display_name + ' has left the Queue!'), color=0xf55742)
        await ctx.send(embed=embed)
        part = que[id].remove(x)
        parts = part
        """cell_list1 = sheet.findall(str(userid))
        cell_list2 = sheet.findall(nick)
        value1 = cell_list1[0]
        value2 = cell_list2[0]
        sheet.update_cell(value1.row, value1.col, '-')
        sheet.update_cell(value2.row, value2.col, 'N/A')"""
        if sheet11.findall(nick):
            cell = sheet11.find(nick)
            row_number = cell.row
            print(cell.row)
            workbook2_row = 'C'+str(row_number)
            print(workbook2_row)
            sheet11.update_acell(workbook2_row, ('FALSE'))
        else:
            print('watchu talkin about willis')

    @commands.command()
    async def replace(self, ctx, member: discord.Member, member_rep: discord.Member):
        name1 = member.display_name
        name2 = member_rep.display_name
        id1 = member.id
        id2 = member_rep.id
        cell_list1 = sheet11.findall(str(id1))
        cell_list2 = sheet11.findall(name1)
        value1 = cell_list1[0]
        value2 = cell_list2[0]
        sheet11.update_cell(value1.row, value1.col, id2)
        sheet11.update_cell(value2.row, value2.col, name2)

    """__________________Queue__________________"""

    @commands.command()
    async def queue(self, ctx):

        if len(que) <= 0:
            embed = discord.Embed(
                title=('Queue is Empty!' + '\n' + '!join to Part'), color=0xf55742)
            await ctx.send(embed=embed)
        else:
            amount = len(que[id])
            print(amount)
            queholder = que[id]
            performingnow = queholder[0]
            embed = discord.Embed(
                title=('Now | ' + performingnow), description=(f'**__{str(amount)} Total Participants__**' + '\n' + ("\n".join(que[id]))), color=0x7289da)
            await ctx.send(embed=embed)

    """__________________Add & Kick for Host Only__________________"""

    @ commands.command()
    async def add(self, ctx, member: discord.Member):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            global parts
            global que
            part = member.display_name
            role = discord.utils.get(member.guild.roles, name="Participant")
            await discord.Member.add_roles(member, role)
            insertRow = [part]
            if not sheet.findall(part):
                sheet.append_row(insertRow, table_range='A2')
            else:
                print('found a match')
            parts = part
            if id in que:
                que[id].append(part)
            else:
                que[id] = [part]
            embed = discord.Embed(
                title=(part + ' has been Added to the Queue'), color=0xaaf542)
            await ctx.send(embed=embed)
        else:
            await ctx.send('This command is only for the Host!')

    @ commands.command()
    async def kick(self, ctx, member: discord.Member):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            global parts
            role = discord.utils.get(member.guild.roles, name="Participant")
            await discord.Member.remove_roles(member, role)
            x = member.display_name
            print('Position', x)
            part = que[id].remove(x)
            parts = part
            embed = discord.Embed(
                title=(x + ' has been kicked from the Queue!'), color=0xf55742)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=('This command is only for the Host!'), color=0xf55742)
            await ctx.send(embed=embed)

    """__________________Lock & Unlock for Host Only__________________"""

    @ commands.command()
    async def close(self, ctx):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            global locked
            locked = True
            embed = discord.Embed(
                title=('The Queue is now Locked!'), color=0xf55742)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=('This command is only for the Host!'), color=0xf55742)
            await ctx.send(embed=embed)

    @ commands.command()
    async def open(self, ctx):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            global locked
            locked = False
            embed = discord.Embed(
                title=('The Queue is now Unlocked!'), color=0xaaf542)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=('This command is only for the Host!'), color=0xf55742)
            await ctx.send(embed=embed)

    """__________________Next, Skip, & End for Host Only__________________"""

    @ commands.command()
    async def next(self, ctx):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            global parts
            part = que[id].pop(0)
            parts = part
            queholder = que[id]
            performingnow = queholder[0]

            amount = len(que[id])
            embed = discord.Embed(
                title=(performingnow + ' | is UP'), description=(f'**__{str(amount)} Total Participants__**' + '\n' + ("\n".join(que[id]))), color=0x7289da)
            await ctx.send(embed=embed)
            for user in ctx.guild.members:
                if user.display_name == performingnow:
                    await user.edit(mute=False)

        else:
            embed = discord.Embed(
                title=('This command is only for the Host!'), color=0xf55742)
            await ctx.send(embed=embed)

    @ commands.command()
    async def skip(self, ctx):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            queholder = que[id]
            x = queholder[0]
            embed = discord.Embed(
                title=(x + ' has been skiped!'), color=0xf55742)
            await ctx.send(embed=embed)
            que[id].append(que[id].pop(que[id].index(x)))

            performingnow = queholder[0]
            amount = len(que[id])
            embed = discord.Embed(
                title=('Next Up | ' + performingnow), description=(f'**__{str(amount)} Total Participants__**' + '\n' + ("\n".join(que[id]))), color=0x7289da)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=('This command is only for the Host!'), color=0xf55742)
            await ctx.send(embed=embed)

    @ commands.command()
    async def end(self, ctx):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            que.clear()
            text_channel = self.client.get_channel(678189261656293376)
            embed = discord.Embed(
                title=('The Event is now Over!'), description=(f"**---Please Use {text_channel.mention}---**"), color=0x7289da)
            await ctx.send(embed=embed)
            role_to_remove = "Participant"
            role_2_remove = "BBXINT Daily Judge"
            for user in ctx.guild.members:
                for role in user.roles:
                    if role.name == role_to_remove:
                        await user.remove_roles(role)
                    if role.name == role_2_remove:
                        await user.remove_roles(role)

        else:
            embed = discord.Embed(
                title=('This command is only for the Host!'), color=0xf55742)
            await ctx.send(embed=embed)

    @ commands.command(aliases=['corona', 'covid', 'lk'])
    async def lock(self, ctx, channel: discord.TextChannel = None):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            channel = channel or ctx.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            embed = discord.Embed(
                title=(f'{channel} has been Locked'), color=0xf55742)
            print(channel)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=('This command is only for the Host!'), color=0xf55742)
            await ctx.send(embed=embed)

    @ commands.command(aliases=['ulk'])
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            channel = channel or ctx.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            embed = discord.Embed(
                title=(f'{channel} has been Unlocked'), color=0xaaf542)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=('This command is only for the Host!'), color=0xf55742)
            await ctx.send(embed=embed)

    @commands.command()
    async def flip(self, ctx):
        choices = ["It's Heads", "It's Tails from Portugal"]
        randcoin = random.choice(choices)
        embed = discord.Embed(
            title=(randcoin), color=0x7289da)
        await ctx.send(embed=embed)

    @commands.command()
    async def top16(self, ctx):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            topscore16 = sheet10.col_values(5)
            battlelist = sheet10.col_values(6)
            embed = discord.Embed(
                title=("**TODAY'S TOP 16 & BATTLE BRACKET**"), color=0xff4000)
            embed.add_field(name="Top 16", value=(
                "\n".join(topscore16)), inline=True)
            embed.add_field(name="|", value="**|**", inline=True)
            embed.add_field(name="BATTLE BRACKET", value=(
                "\n".join(battlelist)), inline=True)
            embed.set_author(
                name="BEATBOXINTERNATIONAL.COM", url="https://www.beatboxinternational.com", icon_url="https://lh3.googleusercontent.com/a-/AOh14GiBlYNVkzQLbkdzK-prRDKGmfy2INbA9n3Og0A-Bg=s88")
            message = await ctx.send(embed=embed)
            await message.pin()

    @ commands.command()
    async def top8(self, ctx):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            topscore8 = sheet10.col_values(7)
            battlelist = sheet10.col_values(8)
            embed = discord.Embed(
                title=("**TODAY'S TOP 8 & BATTLE BRACKET**"), color=0xff4000)
            embed.add_field(name="Top 8", value=(
                "\n".join(topscore8)), inline=True)
            embed.add_field(name="|", value="**|**", inline=True)
            embed.add_field(name="BATTLE BRACKET", value=(
                "\n".join(battlelist)), inline=True)
            embed.set_author(
                name="BEATBOXINTERNATIONAL.COM", url="https://www.beatboxinternational.com", icon_url="https://lh3.googleusercontent.com/a-/AOh14GiBlYNVkzQLbkdzK-prRDKGmfy2INbA9n3Og0A-Bg=s88")
            message = await ctx.send(embed=embed)
            await message.pin()

    """@ commands.command()
    async def resetsheet(self, ctx):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            range_of_cells = sheet.range('A2:A151')
            for cell in range_of_cells:
                cell.value = ''
            sheet.update_cells(range_of_cells)
            range_of_cells = sheet2.range('C3:G152')
            for cell in range_of_cells:
                cell.value = ''
            sheet2.update_cells(range_of_cells)
            range_of_cells = sheet3.range('C3:G152')
            for cell in range_of_cells:
                cell.value = ''
            sheet3.update_cells(range_of_cells)
            range_of_cells = sheet4.range('C3:G152')
            for cell in range_of_cells:
                cell.value = ''
            sheet4.update_cells(range_of_cells)
            range_of_cells = sheet5.range('C3:G152')
            for cell in range_of_cells:
                cell.value = ''
            sheet5.update_cells(range_of_cells)
            range_of_cells = sheet6.range('C3:G152')
            for cell in range_of_cells:
                cell.value = ''
            sheet6.update_cells(range_of_cells)
            range_of_cells = sheet9.range('F3:F18')
            for cell in range_of_cells:
                cell.value = ''
            sheet9.update_cells(range_of_cells)
            range_of_cells = sheet9.range('E3:E18')
            for cell in range_of_cells:
                cell.value = False
            sheet9.update_cells(range_of_cells)
            range_of_cells = sheet7.range('J3:L5')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('J8:L10')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('J14:L16')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('J20:L22')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('J26:L28')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('O3:Q5')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('O8:Q10')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('O14:Q16')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('O20:Q22')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('T3:V5')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('T8:V10')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('T14:V16')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('Y3:AA5')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('Y8:AA10')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)
            range_of_cells = sheet7.range('Y14:AA16')
            for cell in range_of_cells:
                cell.value = False
            sheet7.update_cells(range_of_cells)

            await ctx.message.delete()

        else:
            embed = discord.Embed(
                title=('This command is only for the Host!'), color=0xf55742)
            await ctx.send(embed=embed)"""

    @ commands.command()
    async def dmsheet(self, ctx):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            await ctx.author.send("Here's the BBXINT Judging Sheet " + '\n' + 'https://docs.google.com/spreadsheets/d/1FAIk6R9Rr12X-DyWlH3Z7vBUV8Ij74qGyTF4n86a66o/edit?usp=sharing')
            await ctx.message.delete()
        else:
            embed = discord.Embed(
                title=('This command is only for the Host!'), color=0xf55742)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(EventQueue(client))
