import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from bot import bot

from banpick import *
from banpick_class import *
from PIL import Image, ImageFont, ImageDraw
from banpick_image import *

# 테스트 할때 사용
load_dotenv()
# GitHub Secrets에서 가져오는 값
TOKEN = os.getenv('DISCORD_TOKEN')


@bot.command(name='밴픽')
async def start_banpick(ctx):
    await ctx.send('밴픽을 시작합니다.')
    # 0. 현재 채널에서 진행되는 내전 있는지 확인 (없다면 에러 처리)
    # 0-1. 밴픽 내용 기록할 dict 생성
    full_game_info = make_new_full_game_info(ctx)
    # 1. 밴픽 진행 / 내전 종료 선택 (되물어보기)
    is_banpick = await generate_new_banpick(ctx, full_game_info)
    # 2. 블루팀, 레드팀 선택
    # 3. 라인 선택 (2번째 게임부터는 이전 게임과 동일 버튼 추가)
    # 4. 밴픽을 진행할 서버원 정하기 (직접 누르는 방식)
    # 5. 챔피언 풀 보여주는 View 띄우고, 1밴부터 3밴까지 블루 - 레드 차례대로 진행
    # 6. 챔피언 픽 진행 , 4,5 밴 진행, 나머지 픽 진행
    # 7. 밴픽 수정사항 있는지 확인. 있다면 수정 (되물어보기)
    # 8. 각 픽에 대해 어떤 서버원이 플레이하는지 선택 (되물어보기)
    # 9. 게임 결과 입력하는 View 띄우기 (되물어보기)


@bot.command(name='테스트')
async def start_test(ctx):
    guild = bot.get_guild(1329305604757393458)
    
    masulsa = guild.get_member(333804390332760064)
    ferrero = guild.get_member(450269424419733515)
    by = guild.get_member(1109093546117562421)
    gahyun = guild.get_member(363957070946500609)
    rp = guild.get_member(282224018021548042)
    jugking = guild.get_member(520854287958409232)
    zeus = guild.get_member(775730233588449330)
    ddoromi = guild.get_member(1000827213349924974)
    seun = guild.get_member(464012166006046721)
    hyeji = guild.get_member(1271827910982107193)
    full_game_info = make_new_full_game_info(ctx)
    full_game_info['host'] = ctx.author
    full_game_info['summoners'] = [masulsa, by, seun, gahyun, zeus, ferrero, jugking, ddoromi, rp, hyeji]
    full_game_info['baron']['members'] = [masulsa, by, seun, gahyun, zeus]
    full_game_info['elder']['members'] = [ferrero, jugking, ddoromi, rp, hyeji]

    full_game_info['leader']['baron'] = masulsa
    full_game_info['leader']['elder'] = rp
    await initiate_banpick(ctx, full_game_info)


@bot.command(name='test')
async def tttt(ctx):

    blue_team_members = ["FERRERO0 #KR1", "T1 zeus #kr222", "236236rp#KR1", "마술사의 수습생 #KR1", "가 현 #1210"]
    red_team_members = ["뭘by녀석아 #KR1", "JUGKING #JP69", "또로미 #030", "세 은#0911", "김혜지 #1994"]
    
    banpick_image = get_background_image(blue_team_members, red_team_members, "마술사의 수습생 #KR1", "뭘by녀석아 #KR1", 1, 1, 3)

    blue_pick = ['aatrox', 'ahri', 'akali', None, None]
    red_pick = ['ambessa', 'amumu', 'anivia', None, None]

    blue_picked_images = get_picked_images(blue_pick)
    red_picked_images = get_picked_images(red_pick)

    blue_ban = ['zyra', 'zoe', 'zilean', None, None]
    red_ban = ['zed', 'zac', 'yuumi', 'yorick', None]

    blue_banned_images = get_banned_images(blue_ban)
    red_banned_images = get_banned_images(red_ban)

    # 밴 합치기
    banpick_image.paste(blue_banned_images, (0, h - pick_y - ban_y))
    banpick_image.paste(red_banned_images, (w - ban_x * 5, h - pick_y - ban_y))

    # 픽 합치기
    banpick_image.paste(blue_picked_images, (0, h - pick_y)) 
    banpick_image.paste(red_picked_images, (w - pick_x * 5, h - pick_y))


    # changseop_image = Image.open('changseop.png').resize((400, 400), Image.LANCZOS)
    # merged_image.paste(changseop_image, (760, 340)) 

    # 이미지를 메모리 내에서 처리
    buffer = io.BytesIO()
    banpick_image.save(buffer, format='PNG')
    buffer.seek(0)  # 스트림의 시작 위치로 이동

    # Discord에 메모리 파일로 전송
    await ctx.send(file=discord.File(buffer, filename="example.png"))


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