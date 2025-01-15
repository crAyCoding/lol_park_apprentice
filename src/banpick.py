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