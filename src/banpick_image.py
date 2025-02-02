from PIL import Image, ImageFont, ImageDraw, ImageOps

def get_title_image(blue_team_members, red_team_members, blue_leader, red_leader, blue_win, red_win, game_number):
    # 이미지 생성
    title_image = Image.new('RGB', (1920, 700), 'pink')
    draw = ImageDraw.Draw(title_image)

    font_path = "assets/fonts/CookieRun.ttf"  # 시스템에 설치된 폰트 파일 경로
    team_font = ImageFont.truetype(font_path, 80) 
    leader_font = ImageFont.truetype(font_path, 45)

    draw.line((0, 200, 1920, 203), fill="black", width=1)

    # 블루팀 텍스트 정렬 (좌측에서 50px)
    draw.text((50, 20), "블루팀", fill='blue', font=team_font)
    draw.text((50, 210), f"   탑 : {blue_team_members[0][:20]}", fill=f"{'purple' if blue_team_members[0] == blue_leader else 'white'}", font=leader_font)
    draw.text((50, 290), f"정글 : {blue_team_members[1][:20]}", fill=f"{'purple' if blue_team_members[1] == blue_leader else 'white'}", font=leader_font)
    draw.text((50, 370), f"미드 : {blue_team_members[2][:20]}", fill=f"{'purple' if blue_team_members[2] == blue_leader else 'white'}", font=leader_font)
    draw.text((50, 450), f"원딜 : {blue_team_members[3][:20]}", fill=f"{'purple' if blue_team_members[3] == blue_leader else 'white'}", font=leader_font)
    draw.text((50, 530), f"서폿 : {blue_team_members[4][:20]}", fill=f"{'purple' if blue_team_members[4] == blue_leader else 'white'}", font=leader_font)

    # 레드팀 텍스트 우측 기준 정렬 (50px 떨어지게)
    image_width = title_image.width

    text_width = draw.textlength('레드팀', font=team_font)
    red_team_x = image_width - text_width - 50
    draw.text((red_team_x, 20), "레드팀", fill="red", font=team_font)

    red_member_1 = image_width - draw.textlength(f"{red_team_members[0][:20]} :    탑", font=leader_font) - 50
    red_member_2 = image_width - draw.textlength(f"{red_team_members[1][:20]} : 정글", font=leader_font) - 50
    red_member_3 = image_width - draw.textlength(f"{red_team_members[2][:20]} : 미드", font=leader_font) - 50
    red_member_4 = image_width - draw.textlength(f"{red_team_members[3][:20]} : 원딜", font=leader_font) - 50
    red_member_5 = image_width - draw.textlength(f"{red_team_members[4][:20]} : 서폿", font=leader_font) - 50
    draw.text((red_member_1, 210), f"{red_team_members[0][:20]} :    탑", fill=f"{'purple' if red_team_members[0] == red_leader else 'white'}", font=leader_font)
    draw.text((red_member_2, 290), f"{red_team_members[1][:20]} : 정글", fill=f"{'purple' if red_team_members[1] == red_leader else 'white'}", font=leader_font)
    draw.text((red_member_3, 370), f"{red_team_members[2][:20]} : 미드", fill=f"{'purple' if red_team_members[2] == red_leader else 'white'}", font=leader_font)
    draw.text((red_member_4, 450), f"{red_team_members[3][:20]} : 원딜", fill=f"{'purple' if red_team_members[3] == red_leader else 'white'}", font=leader_font)
    draw.text((red_member_5, 530), f"{red_team_members[4][:20]} : 서폿", fill=f"{'purple' if red_team_members[4] == red_leader else 'white'}", font=leader_font)

    # 점수 표시 (현 스코어)
    score_font = ImageFont.truetype(font_path, 120)
    score_text = f'{blue_win}   :   {red_win}'
    score_text_width = draw.textlength(score_text, font=score_font)
    score_text_x = (image_width - score_text_width) / 2

    draw.text((score_text_x, 30), score_text, fill='black', font=score_font)

    # 게임 번호 표시
    game_number_font = ImageFont.truetype(font_path, 40)
    game_text_width = draw.textlength(f'GAME {game_number}', font=game_number_font)
    game_text_x = (image_width - game_text_width) / 2
    draw.text((game_text_x, 0), f'GAME {game_number}', fill="black", font=game_number_font)

    return title_image


def get_banned_image(champion_name=None):

    if champion_name:
        ban_image = Image.open(f'assets/lol_champions_square/{champion_name}.png').convert("L").resize((100, 100), Image.LANCZOS)
    else:
        ban_image = Image.new('RGB', (100, 100), 'black')

    width, height = ban_image.size
    draw = ImageDraw.Draw(ban_image)

    # 🔹 대각선 추가 (왼쪽 하단 → 오른쪽 상단)
    draw.line((0, height, width, 0), fill="black", width=10)

    ban_image = ImageOps.expand(ban_image, border=1, fill='white')

    return ban_image


def get_picked_image(champion_name=None):

    if champion_name:
        pick_image = Image.open(f'assets/lol_champions_loading/{champion_name}.jpg').resize((155, 280), Image.LANCZOS)
    else:
        pick_image = Image.new('RGB', (155, 280), 'black')

    pick_image = ImageOps.expand(pick_image, border=1, fill='white')

    return pick_image

