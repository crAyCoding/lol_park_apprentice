# display_name으로부터 `닉네임#태그` 가져오기
def get_nickname(member):
    return member.display_name.split('/')[0].strip()


# 팀 평균 티어 계산하기
def get_avg_tier(team_list: list):
    total_score = sum(get_member_tier_score(member) for member in team_list)
    return score_to_tier(total_score // len(team_list))


# 티어 점수 가져오기
def get_member_tier_score(member) -> int:
    def get_member_tier(member):
        tier = member.display_name.split('/')[1].strip().lstrip('🔺🔻')
        level = tier[:2] if tier.startswith('GM') else tier[0]
        score = int(tier[2:] if level == 'GM' else tier[1:])
        return level, score

    level, score = get_member_tier(member)

    score_by_tier = {
        'C': -score // 10,
        'GM': -score // 10,
        'M': -score // 10,
        'D': score * 10,
        'E': score * 10 + 40,
        'P': score * 10 + 80,
        'G': score * 10 + 120,
        'S': score * 10 + 160,
        'B': score * 10 + 200,
        'I': score * 10 + 240,
    }

    default_score = 300
    return default_score + score_by_tier.get(level, 99999999)  # 언랭은 99999999


# 점수를 티어로 환산
def score_to_tier(score):
    tiers = [
        (180, 'C1200 ↑'), (190, 'C1100 ↑'), (200, 'C1000 ↑'), (210, 'GM900 ↑'),
        (220, 'GM800 ↑'), (230, 'GM700 ↑'), (240, 'M600 ↑'), (250, 'M500 ↑'),
        (260, 'M400 ↑'), (270, 'M300 ↑'), (280, 'M200 ↑'), (290, 'M100 ↑'),
        (300, 'M1 ↑'), (310, 'D1'), (320, 'D2'), (330, 'D3'), (340, 'D4'),
        (350, 'E1'), (360, 'E2'), (370, 'E3'), (380, 'E4'), (390, 'P1'),
        (400, 'P2'), (410, 'P3'), (420, 'P4'), (430, 'G1'), (440, 'G2'),
        (450, 'G3'), (460, 'G4'), (470, 'S1'), (480, 'S2'), (490, 'S3'),
        (500, 'S4'), (510, 'B1'), (520, 'B2'), (530, 'B3'), (540, 'B4'),
        (550, 'I1'), (560, 'I2'), (570, 'I3'), (580, 'I4')
    ]
    for threshold, tier in tiers:
        if score <= threshold:
            return tier
    return 'UR'


# 팀 목록 메시지 출력
def get_team_list(full_game_info):
    def format_team_message(team_name, members):
        avg_tier = get_avg_tier(members)
        member_list = '\n'.join(member.display_name for member in members)
        team_color = f'🟦' if team_name == '바론' else '🟥'
        return f'{team_color} 팀 {team_name} ( 평균 티어 : {avg_tier} )\n\n{member_list}\n\n'

    baron_members = full_game_info['baron']['members']
    elder_members = full_game_info['elder']['members']

    message = f'# 내전 N 팀 목록\n```\n'
    message += format_team_message('바론', baron_members)
    message += format_team_message('장로', elder_members)
    message += '```'
    return message
