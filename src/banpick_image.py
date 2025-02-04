from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageFont
from functions import get_nickname

w = 1920
h = 1080

title_x_padding = 50
title_y_padding = 20

ban_x = 100
ban_y = 100
pick_x = 155
pick_y = 280


def get_banpick_image(full_game_info, present_game, game_number):

    banpick_image = Image.new('RGB', (w, h), 'pink')

    blue_team = present_game['blue']
    red_team = present_game['red']

    blue_members = full_game_info[blue_team]['members']
    red_members = full_game_info[red_team]['members']

    blue_banpick_host = present_game['blue_host']
    red_banpick_host = present_game['red_host']
    blue_win = full_game_info['blue_win']
    red_win = full_game_info['red_win']

    blue_ban = present_game['blue_ban']
    red_ban = present_game['red_ban']

    blue_pick = present_game['blue_pick']['picked']
    red_pick = present_game['red_pick']['picked']

    banpick_image.paste(get_background_image(present_game, blue_banpick_host, red_banpick_host, blue_win, red_win, game_number))

    # 밴 합치기
    banpick_image.paste(get_banned_images(blue_ban), (0, h - pick_y - ban_y))
    banpick_image.paste(get_banned_images(red_ban), (w - ban_x * 5, h - pick_y - ban_y))

    # 픽 합치기
    banpick_image.paste(get_picked_images(blue_pick), (0, h - pick_y)) 
    banpick_image.paste(get_picked_images(red_pick), (w - pick_x * 5, h - pick_y))

    return banpick_image


def draw_team(draw, team_name, present_game, leader, align="left", font=None):

    team_x_pos = title_x_padding if team_name == "블루팀" else w - draw.textlength("레드팀", font=font["team"]) - title_x_padding
    leader_x_pos = title_x_padding
    line_names = ["탑", "정글", "미드", "원딜", "서폿"]
    
    for i, line in enumerate(line_names):
        nickname = present_game[f'{"blue" if team_name == "블루팀" else "red"}_pick'][line]['summoner'].split('/')[0].strip()
        text = f"{line_names[i]} : {nickname[:20]}" if align == "left" else f"{nickname[:20]} : {line_names[i]}"
        color = "purple" if nickname == get_nickname(leader) else "white"

        if align == "right":
            leader_x_pos = w - draw.textlength(text, font=font["leader"]) - title_x_padding
        
        draw.text((leader_x_pos, title_y_padding + 220 + (i * 80)), text, fill=color, font=font["leader"])

    draw.text((team_x_pos, title_y_padding), team_name, fill="blue" if team_name == "블루팀" else "red", font=font["team"])


def get_background_image(present_game, blue_banpick_host, red_banpick_host, blue_win, red_win, game_number):

    title_image = Image.new('RGB', (w, h), 'pink')
    draw = ImageDraw.Draw(title_image)

    font_path = "assets/fonts/CookieRun.ttf"
    font = {
        "team": ImageFont.truetype(font_path, 80),
        "leader": ImageFont.truetype(font_path, 45),
        "score": ImageFont.truetype(font_path, 120),
        "game": ImageFont.truetype(font_path, 40),
        "director": ImageFont.truetype(font_path, 40)
    }

    # 구분선
    draw.line((0, 200, w, 203), fill="black", width=1)

    # 블루팀 & 레드팀 정보 표시

    draw_team(draw, "블루팀", present_game, blue_banpick_host, align="left", font=font)
    draw_team(draw, "레드팀", present_game, red_banpick_host, align="right", font=font)

    # 점수 표시
    score_text = f'{blue_win}   :   {red_win}'
    score_x = (w - draw.textlength(score_text, font=font["score"])) / 2
    draw.text((score_x, 30), score_text, fill='black', font=font["score"])

    # 게임 번호 표시
    game_text = f'GAME {game_number}'
    game_x = (w - draw.textlength(game_text, font=font["game"])) / 2
    draw.text((game_x, 0), game_text, fill="black", font=font["game"])

    # 제작자 표시
    draw.text(((w - draw.textlength("made by", font=font["director"])) / 2, h - 130), "made by", fill='skyblue', font=font["director"])
    draw.text(((w - draw.textlength("마술사의 수습생", font=font["director"])) / 2, h - 80), "마술사의 수습생", fill='skyblue', font=font["director"])

    return title_image



def get_personal_banned_image(champion_name=None):

    if champion_name:
        ban_image = Image.open(f'assets/lol_champions_square/{champion_name}.png').convert("L").resize((ban_x, ban_y), Image.LANCZOS)
    else:
        ban_image = Image.new('RGB', (ban_x, ban_y), 'black')

    width, height = ban_image.size
    draw = ImageDraw.Draw(ban_image)

    # 대각선 추가 (왼쪽 하단 → 오른쪽 상단)
    draw.line((0, height, width, 0), fill="black", width=10)

    ban_image = ImageOps.expand(ban_image, border=1, fill='white')

    return ban_image


def get_personal_picked_image(champion_name=None):

    if champion_name:
        pick_image = Image.open(f'assets/lol_champions_loading/{champion_name}.jpg').resize((pick_x, pick_y), Image.LANCZOS)
    else:
        pick_image = Image.new('RGB', (pick_x, pick_y), 'black')

    pick_image = ImageOps.expand(pick_image, border=1, fill='white')

    return pick_image


def get_banned_images(banned_list):
    banned_images = Image.new('RGB', (ban_x * 5, ban_y))
    
    for index, champion_name in enumerate(banned_list):
        ban_image = get_personal_banned_image(champion_name)
        banned_images.paste(ban_image, (ban_image.width * index, 0))

    return banned_images


def get_picked_images(picked_list):

    picked_images = Image.new('RGB', (pick_x * 5, pick_y))
    
    for index, champion_name in enumerate(picked_list):
        pick_image = get_personal_picked_image(champion_name)
        picked_images.paste(pick_image, (pick_image.width * index, 0))

    return picked_images
