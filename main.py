import os
import discord
from discord.ext import commands
from discord import app_commands
import audioop
from flask import Flask
from threading import Thread

# 🌐 ตั้งค่า Flask Server สำหรับให้แอปออนไลน์ตลอด 24 ชม.
app = Flask(__name__)

@app.route('/')
def home():
    return "Server is running!"

def reu():
    app.run(host='0.0.0.0', port=8080)

def server_no():
    t = Thread(target=reu)
    t.start()


server_no()


GUILD_ID = 1320391859322753075
CHANNEL_ID = 1320391859322753082
HISTORY_CHANNEL_ID = 1320391859754897480
ROLE_ID = 1324684543709413498

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    
    stream_url = 'https://www.twitch.tv/your_channel'
    stream_status = discord.Streaming(name="กำลังสตรีมเกมสนุกๆ!", url=stream_url)

    await bot.change_presence(activity=stream_status)

    channel = bot.get_channel(CHANNEL_ID)
    if channel is not None:
        button = discord.ui.Button(style=discord.ButtonStyle.primary, label="รับยศ✨", custom_id="give_role", emoji="🎮")
        view = discord.ui.View()
        view.add_item(button)

        embed = discord.Embed(
            title="🎉 คลิกปุ่มด้านล่างเพื่อรับยศ! 🎮",
            description="กดปุ่มด้านล่างเพื่อรับยศหรือยกเลิกยศของคุณ!",
            color=discord.Color.blue()
        )
        embed.set_footer(text="สนุกกับการเล่นเกมและการรับยศ!", icon_url="https://example.com/your-footer-icon.png")
        embed.set_thumbnail(url="https://th.bing.com/th/id/R.37b22ed731027b6984fba0f935b5b0d4?rik=d2Ke2x8t6gGwZA&pid=ImgRaw&r=0")
        embed.set_image(url="https://i.pinimg.com/originals/b0/bd/ab/b0bdabdb366b66f6840405500b1b5d82.gif")

        await channel.send(embed=embed, view=view)
    else:
        print(f"ไม่พบห้องที่มี ID {CHANNEL_ID}")

@bot.event
async def on_interaction(interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data['custom_id'] == 'give_role':
            user = interaction.user
            role = discord.utils.get(user.guild.roles, id=ROLE_ID)

            embed = discord.Embed(title="🚀 สถานะยศของคุณ", color=discord.Color.green())

            if role in user.roles:
                await user.remove_roles(role)
                embed.description = f"คุณได้ยกเลิกยศ **{role.name}** แล้ว! 😔"
                embed.color = discord.Color.red()
                embed.set_footer(text="ยกเลิกยศเรียบร้อยแล้ว! ❌")
            else:
                await user.add_roles(role)
                embed.description = f"คุณได้รับยศ **{role.name}** แล้ว! 🎉"
                embed.color = discord.Color.green()
                embed.set_footer(text="คุณได้รับยศแล้ว! ✅")

            await user.send(embed=embed)
            await interaction.response.send_message("(❤´艸｀❤)! 🎮", ephemeral=True)

            history_channel = bot.get_channel(HISTORY_CHANNEL_ID)
            if history_channel is not None:
                history_embed = discord.Embed(
                    title="📜 ประวัติการรับยศ",
                    description=f"**{user.name}** ได้รับยศ/ยกเลิกยศ **{role.name}**",
                    color=discord.Color.purple()
                )
                history_embed.set_thumbnail(url=user.avatar.url)
                history_embed.set_footer(text=f"ID ผู้ใช้: {user.id}", icon_url=user.avatar.url)
                await history_channel.send(embed=history_embed)
            else:
                print(f"ไม่พบห้องประวัติที่มี ID {HISTORY_CHANNEL_ID}")


bot.run(os.getenv('TOKEN'))
