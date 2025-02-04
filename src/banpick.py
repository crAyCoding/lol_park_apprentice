import io
import discord
from banpick_class import make_new_full_game_info, make_new_game_info
from banpick_image import get_banpick_image
from functions import *


banpick_message = None
banpick_turn = None


# 밴픽 시작
async def initiate_banpick(ctx, full_game_info):

    # 팀 목록 메세지 출력
    await ctx.send(get_team_list(full_game_info))

    await generate_new_banpick(ctx, full_game_info)


# 1. 밴픽 진행 / 내전 종료 선택 (되물어보기)
async def generate_new_banpick(ctx, full_game_info: dict):

    # 새 밴픽 진행 여부 view
    generate_banpick_view = discord.ui.View()
    check_new_banpick_view = discord.ui.View()

    # 첫번째 버튼 콜백
    async def first_button_callback(interaction: discord.Interaction):
        if interaction.user != full_game_info["host"]:
            await interaction.response.send_message(
                content='내전 연 사람만 누를 수 있습니다.',
                ephemeral=True 
            )
            return
        full_game_info["resume"] = True if interaction.data['custom_id'] == 'generate' else False
        await interaction.message.delete()
        await ctx.send(content=f'## {"새 밴픽을 시작하시겠습니까?" if full_game_info["resume"] else "내전을 종료하시겠습니까?"}', view=check_new_banpick_view)

    # 두번째 버튼 콜백
    async def second_button_callback(interaction: discord.Interaction):
        if interaction.user != full_game_info["host"]:
            await interaction.response.send_message(
                content='내전 연 사람만 누를 수 있습니다.',
                ephemeral=True 
            )
            return
        result = True if interaction.data['custom_id'] == 'yes' else False
        await interaction.message.delete()
        if result:
            if full_game_info["resume"]:
                # 밴픽 새로이 진행 
                full_game_info["games"].append(make_new_game_info(full_game_info))
                await choose_blue_red(ctx, full_game_info)

                # 테스트용
                print(f'1번 단계 종료\n=======================\n{full_game_info}\n=======================')
            else:
                # 기록지 출력
                await interaction.message.delete()
                await ctx.send(f'밴픽이 종료되었습니다.')
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
        label="네",
        style=discord.ButtonStyle.primary,
        custom_id="yes",
    )
    yes_button.callback = second_button_callback
    check_new_banpick_view.add_item(yes_button)

    # 아니다 버튼
    no_button = discord.ui.Button(
        label="아니오",
        style=discord.ButtonStyle.danger,
        custom_id="no",
    )
    no_button.callback = second_button_callback
    check_new_banpick_view.add_item(no_button)

    await ctx.send(content=f"## 버튼을 선택해주세요.", view=generate_banpick_view)



# 2. 블루팀, 레드팀 선택
async def choose_blue_red(ctx, full_game_info: dict):
    
    # 현재 진행하는 게임 번호 (몇번째인지)
    game_number = len(full_game_info["games"])
    
    if game_number > 1:
        choose_team = full_game_info[f'game_{game_number - 1}']['loser_team']
    else:
        choose_team = 'baron'
    
    present_game = full_game_info["games"][game_number - 1]
    
    leader = full_game_info["leader"][choose_team]

    # View를 인라인으로 정의
    team_choose_view = discord.ui.View()

    # 버튼 핸들러 정의
    def create_button_callback(leader):
        async def button_callback(interaction: discord.Interaction):
            team = interaction.data['custom_id']
            if interaction.user != leader:
                await interaction.response.send_message(
                    content=f'{get_nickname(leader)}님만 누를 수 있습니다.',
                    ephemeral=True  # 이 옵션으로 메시지를 요청한 사용자에게만 보이게 설정
                )
                return
            await interaction.message.delete()
            target_team, other_team = ("blue", "red") if team == "블루" else ("red", "blue")
            present_game[target_team] = choose_team
            present_game[other_team] = "baron" if choose_team == "elder" else "elder"
            await interaction.channel.send(f'{get_nickname(leader)}님께서 {team}를 선택하셨습니다.')
            await choose_line(ctx, full_game_info, present_game, game_number)

            # 테스트용
            print(f'2번 단계 종료\n=======================\n{full_game_info}\n=======================')
        return button_callback

    # 블루팀 버튼 추가
    blue_button = discord.ui.Button(
        label="블루팀",
        style=discord.ButtonStyle.primary,
        custom_id="블루",
    )
    blue_button.callback = create_button_callback(leader)
    team_choose_view.add_item(blue_button)

    # 레드팀 버튼 추가
    red_button = discord.ui.Button(
        label="레드팀",
        style=discord.ButtonStyle.danger,
        custom_id="레드"
    )
    red_button.callback = create_button_callback(leader)
    team_choose_view.add_item(red_button)

    await ctx.send(content=f"## {get_nickname(leader)}님, 진영을 선택해주세요.", view=team_choose_view)


# 3. 라인 선택 (2번째 게임부터는 이전 게임과 동일 버튼 추가)
async def choose_line(ctx, full_game_info: dict, present_game: dict, game_number: int):
    
    # 첫번째 게임이 아닌지 여부
    is_not_first_game = True if game_number > 1 else False

    blue_line = []
    red_line = []
    positions = ["top", "jungle", "mid", "bot", "support"]

    if is_not_first_game:
        prev_game = full_game_info["games"][game_number - 2]
        if prev_game['blue'] == present_game['blue']:
            blue_line.extend([prev_game["blue_pick"][pos]["summoner"] for pos in positions])
            red_line.extend([prev_game["red_pick"][pos]["summoner"] for pos in positions])
        else:
            blue_line.extend([prev_game["red_pick"][pos]["summoner"] for pos in positions])
            red_line.extend([prev_game["blue_pick"][pos]["summoner"] for pos in positions])
    else:
        if present_game['blue'] == 'baron':
            blue_line = full_game_info["baron"]["members"]
            red_line = full_game_info["elder"]["members"]
        else:
            blue_line = full_game_info["elder"]["members"]
            red_line = full_game_info["baron"]["members"]

    class LineChooseView(discord.ui.View):
        def __init__(self, line_members, team):
            super().__init__(timeout=3600)
            self.lines = ['탑', '정글', '미드', '원딜', '서폿']
            self.line_members = line_members
            self.answers = {line: member.display_name for line, member in zip(self.lines, line_members)}

            for idx, line in enumerate(self.lines):
                self.add_item(self.create_select(line, line_members[idx], team))
            

        def create_select(self, line, member, team):
            async def callback(interaction: discord.Interaction):
                press_user = interaction.user
                if press_user not in self.line_members:
                    await interaction.response.edit_message(view=self)
                    await interaction.followup.send(
                        f"{'블루' if team == 'blue' else '레드'}팀만 변경이 가능합니다.",
                        ephemeral=True
                    )
                    return
                prev_value = self.answers[line]
                selected_value = interaction.data["values"][0]
                # 다른 Select 옵션 및 placeholder 업데이트
                for child in self.children:
                    if isinstance(child, discord.ui.Select) and child != select:
                        child_line = child.placeholder.split(":")[0].strip()
                        child_member_nickname = child.placeholder.split(":")[1].strip()
                        if child.placeholder == selected_value:
                            for origin_line in self.answers.keys():
                                if origin_line == child_line:
                                    self.answers[child_line] = prev_value
                self.answers[line] = selected_value
                select.placeholder = f"{line} : {selected_value}"
                select.options = [discord.SelectOption(label=line_member.display_name) for line_member in self.line_members if line_member != selected_value]
                await interaction.response.edit_message(view=self)

            select = discord.ui.Select(
                placeholder=f"{line} : {get_nickname(member)}",
                options=[discord.SelectOption(label=line_member.display_name) for line_member in self.line_members],
                min_values=1,
                max_values=1
            )
            select.callback = callback
            return select
        
    class ConfirmView(discord.ui.View):
        def __init__(self, blue_answers, red_answers, blue_message, red_message, blue_members, red_members):
            super().__init__(timeout=3600)
            self.blue = blue_answers
            self.red = red_answers
            self.blue_message = blue_message
            self.red_message = red_message

            self.add_item(self.create_confirm_button('blue', blue_members, red_members))
            self.add_item(self.create_confirm_button('red', blue_members, red_members))
        
        def create_confirm_button(self, team, blue_members, red_members):
            async def callback(interaction: discord.Interaction):
                press_user = interaction.user
                line_members = blue_members if team == 'blue' else red_members
                if press_user not in line_members:
                    await interaction.response.defer()
                    await interaction.followup.send(
                        f"{'블루' if team == 'blue' else '레드'}팀 사람만 누를 수 있습니다.",
                        ephemeral=True
                    )
                    return 
                if team == 'blue':
                    await self.blue_message.delete()
                else:
                    await self.red_message.delete()
                self.remove_item(button)
                if len(self.children) == 0:
                    await interaction.message.delete()
                    await choose_who_banpick(ctx, full_game_info, present_game, game_number, self.blue, self.red)

                    # 테스트용
                    print(f'3번 단계 종료\n=======================\n{full_game_info}\n=======================')
                await interaction.response.edit_message(view=self)

            button_style = discord.ButtonStyle.success if team == 'blue' else discord.ButtonStyle.red
            button = discord.ui.Button(label=f"{'블루' if team == 'blue' else '레드'}팀 확정", style=button_style)
            button.callback = callback
            return button
        
    blue_view = LineChooseView(blue_line)
    red_view = LineChooseView(red_line)
    baron_message = await ctx.send("## 블루팀 라인을 골라주세요.", view=blue_view)
    elder_message = await ctx.send("## 레드팀 라인을 골라주세요.", view=red_view)

    # 결과 확인 버튼을 별도의 View로 추가
    confirm_view = ConfirmView(blue_view.answers, red_view.answers, baron_message, elder_message, blue_line, red_line)
    await ctx.send("확정 버튼을 눌러 선택을 완료하세요:", view=confirm_view)


# 4. 밴픽 진행할 인원 선정
async def choose_who_banpick(ctx, full_game_info, present_game, game_number, blue_line, red_line):
    def get_line_confirm_message():
        def format_team(team_name, team_data):
            team_header = f'🟦 블루팀' if team_name == "blue" else f'🟥 레드팀'
            team_lines = '\n'.join([f'{line} : {member}' for line, member in team_data.items()])
            return f'{team_header}\n\n{team_lines}\n'

        confirm_message = (
            f'```\n'
            f'GAME {game_number}\n\n'
            f'{format_team("blue", blue_line)}\n'
            f'{format_team("red", red_line)}```'
        )

        return confirm_message

    
    line_confirm_message = get_line_confirm_message()

    class WhoBanpickView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=3600)

            # 바론 팀 선택 버튼
            self.add_item(self.create_who_banpick_button('blue'))
            # 장로 팀 선택 버튼
            self.add_item(self.create_who_banpick_button('red'))
            # 이전으로 돌아가기(수정) 버튼
            self.add_item(self.create_undo_button())


        def create_who_banpick_button(self, team):
            async def callback(interaction: discord.Interaction):
                press_user = interaction.user
                team_type = present_game[team]
                if press_user not in full_game_info[team_type]['members']:
                    await interaction.response.defer()
                    await interaction.followup.send(
                        f"{'블루' if team == 'blue' else '레드'}팀 사람만 누를 수 있습니다.",
                        ephemeral=True
                    )
                    return
                self.remove_item(button)
                present_game[f'{team}_host'] = press_user 
                confirmed_line = blue_line if team == 'blue' else red_line
                for (line, member) in confirmed_line.items():
                    present_game[f'{team}_pick'][line]['summoner'] = member
                if len(self.children) == 1:
                    await interaction.message.delete()
                    # 밴픽 진행
                    await progress_banpick(ctx, full_game_info, present_game, game_number)

                    # 테스트용
                    print(f'4번 단계 종료\n=======================\n{full_game_info}\n=======================')
                    return
                await interaction.response.edit_message(view=self)

            button = discord.ui.Button(label=f"{'블루' if team == 'blue' else '레드'}팀 밴픽 진행", style=discord.ButtonStyle.primary)
            button.callback = callback
            return button
        
        def create_undo_button(self):
            async def callback(interaction: discord.Interaction):
                press_user = interaction.user
                if press_user not in full_game_info['summoners']:
                    await interaction.response.defer()
                    await interaction.followup.send(
                        f'내전에 참여하는 사람만 누를 수 있습니다.',
                        ephemeral=True
                    )
                    return
                await interaction.message.delete()
                # 3번으로 돌아가기
                await choose_line(ctx, full_game_info, present_game, game_number)

            button = discord.ui.Button(label=f"라인 선택 다시하기", style=discord.ButtonStyle.red)
            button.callback = callback
            return button
    
    who_banpick_view = WhoBanpickView()
    await ctx.send(content=line_confirm_message, view=who_banpick_view)


# 5. 밴픽 진행
async def progress_banpick(ctx, full_game_info, present_game, game_number):
    global banpick_message, banpick_turn

    blue_host = present_game['blue_host']
    red_host = present_game['red_host']

    # 밴픽 순서
    banpick_turn = 1
    # 1,3,5,7,10,11,14,16,18,19 블루 숫자
    # 2,4,6,8,9,12,13,15,17,20 레드 숫자
    blue_turn_numbers = [1, 3, 5, 7, 10, 11, 14, 16, 18, 19]
    red_turn_numbers = [2, 4, 6, 8, 9, 12, 13, 15, 17, 20]

    while banpick_turn < 20:
        
        print(banpick_turn)

        banpick_image = get_banpick_image(full_game_info, present_game, game_number)

        # 이미지를 메모리 내에서 처리
        buffer = io.BytesIO()
        banpick_image.save(buffer, format='PNG')
        buffer.seek(0)  # 스트림의 시작 위치로 이동

        if banpick_message:
            await banpick_message.delete()  # 기존 메시지 삭제

        # Discord에 메모리 파일로 전송
        banpick_message = await ctx.send(file=discord.File(buffer, filename="example.png"))
        
        now_host = blue_host if banpick_turn in blue_turn_numbers else red_host

        print(now_host.display_name)

        def check_banpick(message):
            
            if message.author != now_host or message.channel != ctx.channel:
                return False

            # 유찰 또는 종료 조건
            if message.content in ['아트록스']:
                return True
            
            return False

        host_message = await ctx.bot.wait_for('message', check=check_banpick)
        champion = 'aatrox'

        if banpick_turn == 1:
            present_game["blue_ban"][0] = champion
        
        banpick_turn = banpick_turn + 1

 



    