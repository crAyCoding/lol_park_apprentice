import discord
from banpick_class import Team, TeamPick

# 내전 전체 밴픽 Dict 생성
def make_new_full_game_info(ctx):
    full_game_info = {
        "channel": ctx.channel.id, # 내전 진행중인 채널
        "host": None, # 내전을 연 사람
        "summoners": [], # 모든 소환사 목록
        "baron": Team('baron', None, []).to_dict(), # 팀 바론 목록
        "elder": Team('elder', None, []).to_dict(), # 팀 장로 목록
        "leader": {"baron": None, "elder": None}, # 팀장
        "games": [], # 각 내전 게임들 담은 list
        "resume": True, # 밴픽 진행 여부
    }
    return full_game_info


# 내전 게임 당 밴픽 Dict 생성
def make_new_game_info(full_game_info):
    game_info = {
        "blue": None,
        "red": None,
        "blue_host": None,
        "red_host": None,
        "blue_ban": [],
        "red_ban": [],
        "pick_order": [],
        "blue_pick": TeamPick().to_dict(),
        "red_pick": TeamPick().to_dict(), 
        "winner": None,
        "loser": None,
    }
    return game_info


# 1. 밴픽 진행 / 내전 종료 선택 (되물어보기)
async def generate_new_banpick(ctx, full_game_info: dict):

    # 새 밴픽 진행 여부 view
    generate_banpick_view = discord.ui.View()
    check_new_banpick_view = discord.ui.View()

    # 첫번째 버튼 콜백
    async def first_button_callback(interaction: discord.Interaction):
        full_game_info["resume"] = True if interaction.data['custom_id'] == 'generate' else False
        await interaction.message.delete()
        await ctx.send(content=f'## {"새로운 게임 밴픽을 시작하시겠습니까?" if full_game_info["resume"] else "내전을 종료하시겠습니까?"}', view=check_new_banpick_view)

    # 두번째 버튼 콜백
    async def second_button_callback(interaction: discord.Interaction):
        result = True if interaction.data['custom_id'] == 'yes' else False
        await interaction.message.delete()
        if result:
            if full_game_info["resume"]:
                # 밴픽 새로이 진행 
                full_game_info["games"].append(make_new_game_info(full_game_info))
                await choose_blue_red(ctx, full_game_info)
            else:
                # 기록지 출력
                print('hi')
        else:
            await ctx.send(content=f"## 버튼을 선택해주세요.", view=generate_banpick_view)
    
    # 밴픽 진행 버튼
    generate_button = discord.ui.Button(
        label="밴픽 진행",
        style=discord.ButtonStyle.primary,
        custom_id="generate",
    )
    generate_button.callback = first_button_callback
    generate_banpick_view.add_item(generate_button)

    # 내전 종료 버튼
    end_button = discord.ui.Button(
        label="내전 종료",
        style=discord.ButtonStyle.green,
        custom_id="end",
    )
    end_button.callback = first_button_callback
    generate_banpick_view.add_item(end_button)
    
    # 그렇다 버튼
    yes_button = discord.ui.Button(
        label="그렇다",
        style=discord.ButtonStyle.primary,
        custom_id="yes",
    )
    yes_button.callback = second_button_callback
    check_new_banpick_view.add_item(yes_button)

    # 아니다 버튼
    no_button = discord.ui.Button(
        label="아니다",
        style=discord.ButtonStyle.danger,
        custom_id="no",
    )
    no_button.callback = second_button_callback
    check_new_banpick_view.add_item(no_button)

    await ctx.send(content=f"## 버튼을 선택해주세요.", view=generate_banpick_view)



# 2. 블루팀, 레드팀 선택
async def choose_blue_red(ctx, full_game_info: dict):
    
    # 현재 진행하는 게임 번호
    game_number = len(full_game_info["games"])
    
    if game_number > 1:
        choose_team = full_game_info[f'game_{game_number - 1}']['loser_team']
    else:
        choose_team = 'baron'
    
    present_game = full_game_info["games"][game_number - 1]
    
    # leader = full_game_info["leader"][choose_team]
    leader = ctx.author

    # View를 인라인으로 정의
    team_choose_view = discord.ui.View()

    # 버튼 핸들러 정의
    async def button_callback(interaction: discord.Interaction):
        team = interaction.data['custom_id']
        await interaction.message.delete()
        target_team, other_team = ("blue", "red") if team == "블루" else ("red", "blue")
        present_game[target_team] = choose_team
        present_game[other_team] = "baron" if choose_team == "elder" else "elder"
        await interaction.channel.send(f'{leader.display_name}님께서 {team}를 선택하셨습니다.')

    # 블루팀 버튼 추가
    blue_button = discord.ui.Button(
        label="블루팀",
        style=discord.ButtonStyle.primary,
        custom_id="블루",
    )
    blue_button.callback = button_callback
    team_choose_view.add_item(blue_button)

    # 레드팀 버튼 추가
    red_button = discord.ui.Button(
        label="레드팀",
        style=discord.ButtonStyle.danger,
        custom_id="레드"
    )
    red_button.callback = button_callback
    team_choose_view.add_item(red_button)

    await ctx.send(content=f"## {leader.display_name}님, 진영을 선택해주세요.", view=team_choose_view)


# 3. 라인 선택 (2번째 게임부터는 이전 게임과 동일 버튼 추가)
async def choose_line(ctx, full_game_info: dict):
    
    # 첫번째 게임이 아닌지 여부
    is_not_first_game = True
    
    if len(full_game_info["games"]) == 1:
        is_not_first_game = False
        
    