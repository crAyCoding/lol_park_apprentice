class Team:
    def __init__(self, name, leader, members):
        self.name = name
        self.leader = leader
        self.members = members
        self.avg_tier = get_average_tier(members)
    
    def to_dict(self):
        return {
            "name": self.name,
            "leader": self.leader,
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
        self.top = Line().to_dict()
        self.jungle = Line().to_dict()
        self.mid = Line().to_dict()
        self.bot = Line().to_dict()
        self.support = Line().to_dict()
    
    def to_dict(self):
        return {
            "top": self.top,
            "jungle": self.jungle,
            "mid": self.mid,
            "bot": self.bot,
            "support": self.support
        }
        

# 팀 평균 티어 계산
def get_average_tier(members: list):
    # 추후 제작 예정
    return None