import discord
from banpick_class import Team, TeamPick

# 내전 전체 밴픽 Dict 생성
def make_new_full_game_info(ctx):
    full_game_info = {
        "channel": ctx.id,
        "summoners": [],
        "team_baron": Team('baron', None, []).to_dict(),
        "team_elder": Team('elder', None, []).to_dict(),
        "leader": {"team_baron": None, "team_elder": None},
        "games": [],
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


# 2. 블루팀, 레드팀 선택
async def choose_blue_red(ctx, full_game_info: dict, game_number: int, choose_team: str):
    if game_number > 1:
        choose_team = full_game_info[f'game_{game_number - 1}']['loser_team']
        
    # leader = full_game_info[choose_team]["leader"]
    leader = ctx.author

    # View를 인라인으로 정의
    team_choose_view = discord.ui.View()

    # 버튼 핸들러 정의
    async def button_callback(interaction: discord.Interaction):
        team = interaction.data['custom_id']
        await interaction.message.delete()
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
