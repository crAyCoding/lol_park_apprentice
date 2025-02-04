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


def find_champion(champion_kor):

    lol_champion_korean_dict = {
        'aatrox': ['아트록스', '아트'],
        'ahri': ['아리'],
        'akali': ['아칼리'],
        'akshan': ['아크샨'],
        'alistar': ['알리스타', '알리'],
        'ambessa': ['암베사'],
        'amumu': ['아무무'],
        'anivia': ['애니비아'],
        'annie': ['애니'],
        'aphelios': ['아펠리오스', '아펠'],
        'ashe': ['애쉬'],
        'aurelionSol': ['아우렐리온 솔', '아우렐리온솔', '아우솔'],
        'aurora': ['오로라'],
        'azir': ['아지르'],
        'bard': ['바드'],
        'belveth': ['벨베스'],
        'blitzcrank': ['블리츠크랭크', '블리츠', '블츠', '블랭'],
        'brand': ['브랜드'],
        'braum': ['브라움'],
        'briar': ['브라이어'],
        'caitlyn': ['케이틀린', '케틀'],
        'camille': ['카밀'],
        'cassiopeia': ['카시오페아', '카시'],
        'chogath': ['초가스'],
        'corki': ['코르키', '콜키'],
        'darius': ['다리우스', '다리'],
        'diana': ['다이애나'],
        'draven': ['드레이븐', '드븐'],
        'drmundo': ['문도박사', '문도', '문박'],
        'ekko': ['에코'],
        'elise': ['엘리스'],
        'evelynn': ['이블린'],
        'ezreal': ['이즈리얼', '이즈'],
        'fiddlesticks': ['피들스틱', '피들'],
        'fiora': ['피오라'],
        'fizz': ['피즈'],
        'galio': ['갈리오'],
        'gangplank': ['갱플랭크', '갱플'],
        'garen': ['가렌'],
        'gnar': ['나르'],
        'gragas': ['그라가스', '글가', '그라'],
        'graves': ['그레이브즈', '그브'],
        'gwen': ['그웬'],
        'hecarim': ['헤카림'],
        'heimerdinger': ['하이머딩거', '하딩'],
        'illaoi': ['일라오이', '일라'],
        'irelia': ['이렐리아', '이렐'],
        'ivern': ['아이번'],
        'janna': ['잔나'],
        'jarvaniv': ['자르반4세', '자르반 4세', '자르반', '잘반'],
        'jax': ['잭스'],
        'jayce': ['제이스'],
        'jhin': ['진'],
        'jinx': ['징크스', '징키'],
        'kaisa': ['카이사'],
        'kalista': ['칼리스타'],
        'karma': ['카르마'],
        'karthus': ['카서스'],
        'kassadin': ['카사딘'],
        'katarina': ['카타리나', '카타'],
        'kayle': ['케일'],
        'kayn': ['케인'],
        'kennen': ['케넨'],
        'khazix': ['카직스'],
        'kindred': ['킨드레드', '킨드'],
        'kled': ['클레드'],
        'kogmaw': ['코그모'],
        'ksante': ['크산테', '산테'],
        'leblanc': ['르블랑'],
        'leesin': ['리신', '리 신'],
        'leona': ['레오나'],
        'lillia': ['릴리아'],
        'lissandra': ['리산드라', '리산'],
        'lucian': ['루시안'],
        'lulu': ['룰루'],
        'lux': ['럭스'],
        'malphite': ['말파이트', '말파'],
        'malzahar': ['말자하'],
        'maokai': ['마오카이', '마오'],
        'masteryi': ['마스터이', '마스터 이', '마이'],
        'mel': ['멜'],
        'milio': ['밀리오'],
        'missfortune': ['미스 포츈', '미스포츈', '미포'],
        'mordekaiser': ['모데카이저', '모데'],
        'morgana': ['모르가나', '몰가나'],
        'naafiri': ['나피리'],
        'nami': ['나미'],
        'nasus': ['나서스'],
        'nautilus': ['노틸러스', '노틸'],
        'neeko': ['니코'],
        'nidalee': ['니달리'],
        'nilah': ['닐라'],
        'nocturne': ['녹턴'],
        'nunu': ['누누와 윌럼프', '누누와윌럼프', '누누'],
        'olaf': ['올라프'],
        'orianna': ['오리아나', '오리'],
        'ornn': ['오른'],
        'pantheon': ['판테온'],
        'poppy': ['뽀삐'],
        'pyke': ['파이크'],
        'qiyana': ['키아나'],
        'quinn': ['퀸'],
        'rakan': ['라칸'],
        'rammus': ['람머스'],
        'reksai': ['렉사이'],
        'rell': ['렐'],
        'renata': ['레나타 글라스크', '레나타글라스크', '레나타'],
        'renekton': ['레넥톤', '레넥'],
        'rengar': ['렝가'],
        'riven': ['리븐'],
        'rumble': ['럼블'],
        'ryze': ['라이즈'],
        'samira': ['사미라'],
        'sejuani': ['세주아니', '세주'],
        'senna': ['세나'],
        'seraphine': ['세라핀'],
        'sett': ['세트'],
        'shaco': ['샤코'],
        'shen': ['쉔'],
        'shyvana': ['쉬바나'],
        'singed': ['신지드'],
        'sion': ['사이온'],
        'sivir': ['시비르'],
        'skarner': ['스카너'],
        'smolder': ['스몰더'],
        'sona': ['소나'],
        'soraka': ['소라카'],
        'swain': ['스웨인'],
        'sylas': ['사일러스', '사일'],
        'syndra': ['신드라'],
        'tahmkench': ['탐 켄치', '탐켄치', '켄치'],
        'taliyah': ['탈리야', '탈랴'],
        'talon': ['탈론'],
        'taric': ['타릭'],
        'teemo': ['티모'],
        'thresh': ['쓰레쉬', '쓸쉬'],
        'tristana': ['트리스타나', '트리', '트타'],
        'trundle': ['트런들'],
        'tryndamere': ['트린다미어', '트린'],
        'twistedFate': ['트위스티드 페이트', '트위스티드페이트', '트페'],
        'twitch': ['트위치'],
        'udyr': ['우디르'],
        'urgot': ['우르곳'],
        'varus': ['바루스'],
        'vayne': ['베인'],
        'veigar': ['베이가'],
        'velkoz': ['벨코즈'],
        'vex': ['벡스'],
        'vi': ['바이'],
        'viego': ['비에고'],
        'viktor': ['빅토르'],
        'vladimir': ['블라디미르', '블라디'],
        'volibear': ['볼리베어', '볼베'],
        'warwick': ['워윅'],
        'wukong': ['오공'],
        'xayah': ['자야'],
        'xerath': ['제라스'],
        'xinzhao': ['신짜오'],
        'yasuo': ['야스오'],
        'yone': ['요네'],
        'yorick': ['요릭'],
        'yuumi': ['유미'],
        'zac': ['자크'],
        'zed': ['제드'],
        'zeri': ['제리'],
        'ziggs': ['직스'],
        'zilean': ['질리언'],
        'zoe': ['조이'],
        'zyra': ['자이라']
    }

    for key, values in lol_champion_korean_dict.items():
        if champion_kor in values:
            return key
    return None  # 일치하는 챔피언이 없을 경우 None 반환
