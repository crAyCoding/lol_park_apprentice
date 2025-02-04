# 내전 전체 밴픽 Dict 생성
def make_new_full_game_info(ctx):
    full_game_info = {
        "channel": ctx.channel.id, # 내전 진행중인 채널
        "host": None, # 내전을 연 사람
        "summoners": [], # 모든 소환사 목록
        "baron": Team('baron', []).to_dict(), # 팀 바론 목록
        "elder": Team('elder', []).to_dict(), # 팀 장로 목록
        "leader": {"baron": None, "elder": None}, # 팀장
        "games": [], # 각 내전 게임들 담은 list
        "resume": True, # 밴픽 진행 여부
        "game_id": None, # 게임 번호 (저장용)
        "blue_win": 0,
        "red_win": 0
    }
    return full_game_info


# 내전 게임 당 밴픽 Dict 생성
def make_new_game_info(full_game_info):
    game_info = {
        "blue": None, # 'baron' or 'elder'
        "red": None, # 'baron' or 'elder'
        "blue_host": None, # baron 팀 밴픽 진행자
        "red_host": None, # elder 팀 밴픽 진행자
        "blue_ban": [None, None, None, None, None],
        "red_ban": [None, None, None, None, None],
        "pick_order": [None, None, None, None, None, None, None, None, None, None], # 블루 1픽부터 레드 5픽까지 순서대로 나열
        "blue_pick": TeamPick().to_dict(),
        "red_pick": TeamPick().to_dict(), 
        "winner": None,
        "loser": None,
    }
    return game_info


class Team:
    def __init__(self, name, members):
        self.name = name
        self.members = members
        self.avg_tier = get_average_tier(members)
    
    def to_dict(self):
        return {
            "name": self.name,
            "members": self.members,
            "avg_tier": self.avg_tier,
        }
        
class Line:
    def __init__(self):
        self.summoner = None
        self.champion = None
    
    def to_dict(self):
        return {
            "summoner": self.summoner,
            "champion": self.champion
        }

class TeamPick:
    def __init__(self):
        self.picked = [None, None, None, None, None]
        self.top = Line().to_dict()
        self.jungle = Line().to_dict()
        self.mid = Line().to_dict()
        self.bot = Line().to_dict()
        self.support = Line().to_dict()
    
    def to_dict(self):
        return {
            "picked": self.picked,
            "탑": self.top,
            "정글": self.jungle,
            "미드": self.mid,
            "원딜": self.bot,
            "서폿": self.support
        }
        

# 팀 평균 티어 계산
def get_average_tier(members: list):
    # 추후 제작 예정
    return None