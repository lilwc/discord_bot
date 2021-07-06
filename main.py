import discord
from discord.ext import commands
import os
import json
from scrapper import refresh_file_data
from prettytable import PrettyTable

tags_dict = {}
files_dict = {}

client = commands.Bot(command_prefix='!')
client.remove_command("help")

tags_dict, files_dict = refresh_file_data()

@client.event
async def on_ready():
    print('Bot is ready !')


@client.command(aliases=['findtag'])
async def tag(ctx, args):
    txt = "```\n"
    txt += args + "\n"
    i = 0
    for f in tags_dict[args]:
        txt += f + "\n"
        i += 1
        if i >= 15:
            i = 0
            txt += "```"
            await ctx.send(txt)
            txt = "```\n"
    txt += "```"
    await ctx.send(txt)

@client.command(aliases=['findFile'])
async def file(ctx, args):
    txt = "```\n"
    txt += args + "\n"
    txt += "Play Count: " + str(files_dict[args][0]) +  "\n"
    txt += "Description" + "\n"
    txt += str(files_dict[args][2]) +  "\n"
    txt += "```"
    await ctx.send(txt)
    await ctx.send("Link : {}".format(files_dict[args][3]))

@client.command(aliases=['allkeys', 'tags'])
async def alltags(ctx):
    table = PrettyTable()
    table.field_names = ["Tag", "Number of files"]
    i = 0
    for k in tags_dict.keys():
        table.add_row([k, len(tags_dict[k])])
        i += 1
        if i >= 15:
            await ctx.send("```{}```".format(table))
            i = 0
            table = PrettyTable()
            table.field_names = ["Tag", "Number of files"]
    await ctx.send("```{}```".format(table))

@client.command(aliases=['files'])
async def allfiles(ctx):
    table = PrettyTable()
    table.field_names = ["File", "Number of tags", "Play Count"]
    i = 0
    for k in files_dict.keys():
        table.add_row([k, len(files_dict[k][1]), files_dict[k][0]])
        i += 1
        if i >= 15:
            await ctx.send("```{}```".format(table))
            i = 0
            table = PrettyTable()
            table.field_names = ["File", "Number of tags", "Play Count"]
    await ctx.send("```{}```".format(table))

@client.command(aliases=['s'])
async def search(ctx, args):
    table = PrettyTable()
    table.field_names = ["File", "Number of tags", "Play Count"]
    i = 0
    found = False
    for k in files_dict.keys():
        if args.lower() in k.lower():
            found = True
            table.add_row([k, len(files_dict[k][1]), files_dict[k][0]])
            i += 1
        if i >= 15:
            await ctx.send("```{}```".format(table))
            i = 0
            table = PrettyTable()
            table.field_names = ["File", "Number of tags", "Play Count"]
    if found:
        await ctx.send("```{}```".format(table))
    else:
        await ctx.send("```No file containing \'{}\' found```".format(args))

@client.command(aliases=['reload'])
async def refresh(ctx):
    global tags_dict
    global files_dict
    tags_dict, files_dict = refresh_file_data()
    await ctx.send("File list was refreshed !\nNumber of files: {}\nNumber of tags: {}".format(len(files_dict.keys()), len(tags_dict.keys())))

@client.command()
async def pet(ctx):
    await ctx.send("Thank you human ! You deserve a pet as well")


@client.command(aliases=['Help', 'Help Me', 'why'])
async def help(ctx):
    await ctx.send(
        '**Bot Commands**' + '\n' +
        '**!tag** *insert the tag you want*' + '\n' +
        '**!file** *insert the file you want*' + '\n' +
        '**!search** *keyword*' + '\n' +
        '*View all tags*: ' + '**!tags**' + '\n' +
        '*View all files*: ' + '**!files**' + '\n' +
        '*Refresh bot data*: ' + '**!refresh**' + '\n' +
        '**Please note:** tags or file names that are multiple words must be sourrounded by ""'
    )


client.run('ODU5NDk2NzgzNTI0MDAzODYw.YNtiwQ.SBFA4t5q9cq2zVpoKi50F0aYbu4')
