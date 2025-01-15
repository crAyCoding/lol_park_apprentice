import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from bot import bot

# 테스트 할때 사용
load_dotenv()
# GitHub Secrets에서 가져오는 값
TOKEN = os.getenv('DISCORD_TOKEN')


@bot.command(name='밴픽')
async def start_banpick(ctx):
    await ctx.send('밴픽을 시작합니다.')
    # 1. 현재 채널에서 진행되는 내전 있는지 확인
    # 있다면 2번으로, 없다면 에러 처리
    # 2. 블루팀, 레드팀 선택
    # 3. 라인 선택 (2번째 게임부터는 이전 게임과 동일 버튼 추가)
    # 4. 밴픽을 진행할 서버원 정하기 (직접 누르는 방식)
    # 5. 챔피언 풀 보여주는 View 띄우고, 1밴부터 3밴까지 블루 - 레드 차례대로 진행
    # 6. 챔피언 픽 진행 , 4,5 밴 진행, 나머지 픽 진행
    # 7. 밴픽 수정사항 있는지 확인. 있다면 수정 (되물어보기)
    # 8. 각 픽에 대해 어떤 서버원이 플레이하는지 선택 (되물어보기)
    # 9. 게임 결과 입력하는 View 띄우기 (되물어보기)
    # 10. 게임 결과 입력 후 다음 게임 진행 / 내전 종료 선택 (되물어보기)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    

# 명령어 에러 처리
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(f"Unhandled error: {error}")


def main() -> None:
    bot.run(token=TOKEN)


if __name__ == '__main__':
    main()