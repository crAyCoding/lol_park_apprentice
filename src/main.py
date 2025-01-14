import os
import discord
from dotenv import load_dotenv
from bot import bot

# 테스트 할때 사용
load_dotenv()
# GitHub Secrets에서 가져오는 값
TOKEN = os.getenv('DISCORD_TOKEN')


@bot.command(name='밴픽')
async def start_banpick(ctx):
    await ctx.send('밴픽을 시작합니다.')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


def main() -> None:
    bot.run(token=TOKEN)


if __name__ == '__main__':
    main()