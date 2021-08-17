import discord
import os
import subprocess
import pytz
import json
import random
import datetime


from discord import colour as c
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.members = True
intents = discord.Intents.all()

dt_mtn = datetime.datetime.now(tz=pytz.timezone('Asia/Seoul'))

bot = commands.Bot(command_prefix='~', intents=intents)  # 프리픽스 설정

log_channel_id = 828229073636687912  # 원래 봇은 824984470972661800
log_channel = bot.get_channel(log_channel_id)

# if (ctx.channel.id == bot.channel): 이거 준비 해야겠다

# ---------- 색상표 시작 ----------
color_default = 0
teal = c.Colour.teal()
dark_teal = c.Colour.dark_teal()
green = c.Colour.green()
dark_green = c.Colour.dark_green()
blue = c.Colour.blue()
dark_blue = c.Colour.dark_blue()
purple = c.Colour.purple()
dark_purple = c.Colour.dark_purple()
magenta = c.Colour.magenta()
dark_magenta = c.Colour.dark_magenta()
gold = c.Colour.gold()
dark_gold = c.Colour.dark_gold()
orange = c.Colour.orange()
dark_orange = c.Colour.dark_orange()
red = c.Colour.red()
dark_red = c.Colour.dark_red()
lighter_grey = c.Colour.lighter_grey()
dark_grey = c.Colour.dark_grey()
light_grey = c.Colour.light_grey()
darker_grey = c.Colour.darker_grey()
blurple = c.Colour.blurple()
greyple = c.Colour.greyple()


# ---------- 색상표 끝 ----------

# ---------- 이모지표 시작 ----------
# emoji_test =
# ---------- 이모지표 끝 ----------

# 봇이 시작할때 작동
@bot.event
async def on_ready():
    print(bot.user)
    print("봇 로그인 됨")
    print(dt_mtn.strftime('%Y/%m/%d'))
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(name="개발"))

    presence_alarm = bot.get_channel(822368253119561772)

    dt_year = (dt_mtn.strftime('%Y'))
    dt_month = (dt_mtn.strftime('%m'))
    dt_day = (dt_mtn.strftime('%d'))
    dt_time = (dt_mtn.strftime('%X'))

    online = discord.Embed(colour=green, title="<:Stella_Icon:854714421977022495>**Stella Bot Online!**")
    online.add_field(name='현재 핑', value=f'{round(bot.latency * 1000)}ms')
    online.add_field(name='켜진 시간', value=f'{dt_year}/{dt_month}/{dt_day} {dt_time}')

    await presence_alarm.send(embed=online)


# 특정언어 차단

# 굿모닝
@bot.command()
async def 굿모닝(ctx):
    await ctx.send(":white_sun_small_cloud:**좋은 아침입니다!**")

@bot.command()
async def 굿나잇(ctx):
    await ctx.send(":night_with_stars:**오늘도 수고하셨습니다, 좋은 저녁되세요!**")


@bot.command()
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 5, commands.BucketType.guild)
async def dm(ctx, user_id=None, *, args=None):
    if user_id != None and args != None:
        try:
            target = await bot.fetch_user(user_id)
            await target.send(args)

            await ctx.send("'" + args + "'>>> **전송 완료** >>>" + target.name)
            print("'" + target.name + "'에게'" + args + "'를 보냈습니다.")

        except:
            await ctx.send("그 유저에게는 DM을 보낼 수 없습니다!")

    else:
        await ctx.send("에러")


# DM All 기능 (작동 안함)
@bot.command()
@commands.has_permissions(administrator=True)
async def dm_all(ctx, *, args=None):
    if args != None:
        members = ctx.guild.members
        for member in members:
            try:
                await member.send(args)
                print("'" + args + "'>>> 전송 완료 >>>" + member.name)

            except:
                print("그 유저에게는 DM을 보낼 수 없습니다!")

    else:
        await ctx.send("에러")


# Ping 확인
@bot.command()
async def 핑(ctx):
    embed = discord.Embed(colour=blue)
    embed.add_field(name=':green_circle: Stella 봇 핑', value=f'**Ping : {round(bot.latency * 1000)}ms**', inline=True)
    embed.set_footer(text='Stella Bot#9903',
                     icon_url="https://cdn.discordapp.com/avatars/806729801086926869/6d3c0df30e9a81cddf3622e630978b0c.png")
    await ctx.send(embed=embed)


# 킥할 대상을 명령어로 킥함
@bot.command()
@commands.has_permissions(kick_members=True)
async def 킥(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention}님이 **킥** 되었습니다!")
    print("'" + member + "'유저가 Kick 처리 되었습니다")


# 밴할 대상을 명령어로 밴함
@bot.command()
@commands.has_permissions(ban_members=True)
async def 밴(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention}님이 **밴** 되었습니다!")
    print("'" + member + "'유저가 Ban 처리 되었습니다")


# 명령어 확인
@bot.command()
async def 명령어(ctx):
    embed = discord.Embed(colour=purple, title='<:Stella_Icon:854714421977022495> Stella Bot 명령어 리스트')
    embed.add_field(name='상태 관련 명령어', value='~핑, ~서버정보, ~굿모닝, ~굿나잇', inline=False)
    embed.add_field(name='서버 관리 명령어', value='~킥, ~밴, ~공지, ~dm, ~dm_all', inline=False)
    embed.add_field(name='포인트 명령어', value='~출첵, ~출첵순위, ~포인트, ~포인트 순위, 랜덤포인트', inline=False)
    embed.set_footer(text='개발 : Dos0313')
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/806729801086926869/6d3c0df30e9a81cddf3622e630978b0c.png")
    await ctx.send(embed=embed)


# 출첵하기 ------------------------------------------------------ 쿨타임 없음/횟수 표시 안됨
@bot.command(aliases=["ㅊㅊ"])
async def 출첵(ctx):
    if (ctx.channel.id == '771507018301308968'):
        await open_account(ctx.author)

        user = ctx.author
        users = await get_bank_data()

        dt_year = (dt_mtn.strftime('%Y'))
        dt_month = (dt_mtn.strftime('%m'))
        dt_day = (dt_mtn.strftime('%d'))

        cc_point = (50000)

        cc_add_amt = (1)

        cc_amt = users[str(user.id)]["cc_amt"]

        users[str(user.id)]["point"] += cc_point

        users[str(user.id)]["cc_amt"] += cc_add_amt

        with open("point.json", "w") as f:
            json.dump(users, f)

        await ctx.send(
            f"<:Stella_Icon:854714421977022495> `{dt_year}년 {dt_month}월 {dt_day}일` **출석 체크를 완료 하였습니다!** [ <:plusicon:824447751654867005> **{cc_point}** ] [{cc_amt + 1}회]")

        print(f"출첵 이벤트 : {user} + {cc_point}")
        
    else:
        await ctx.send('출석체크 채널로 지정된 곳에서 사용해주세요!')


# ------------------------------------------------------------------------------

# 출첵 순위 확인
@bot.command()
async def 출첵순위(ctx, x=10):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["cc_amt"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(colour=blue, title=f"<:Stella_Icon:854714421977022495>출첵 횟수 Top {x}")
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = bot.get_user(id_)
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f"<:check_box:824447802477772820> {amt}회", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)


@bot.command()
async def 포인트순위(ctx, x=10):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["point"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(colour=blue, title=f"<:Stella_Icon:854714421977022495>포인트 Top {x}")
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = bot.get_user(id_)
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f":regional_indicator_p: {amt}", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)


# 포인트 확인 @bot.command(aliases=["bal"]) 축약 ㅆㄱㄴ이누
@bot.command(aliases=["ㅍㅇㅌ"])
async def 포인트(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    point_amt = users[str(user.id)]["point"]

    point = discord.Embed(type='rich', color=discord.Color.green(), timestamp=ctx.message.created_at)
    point.add_field(name=f"<:Stella_Icon:854714421977022495> {ctx.author.name}님의 Stella 포인트", value=f'{point_amt}P',
                    inline=False)

    await ctx.send(embed=point)


@bot.command(aliases=["ㄹㄷㅍㅇㅌ"])
@commands.cooldown(1, 60, commands.BucketType.user)
async def 랜덤포인트(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()
    earnings = random.randrange(5001)
    await ctx.send(f":regional_indicator_p: **{ctx.author.name}님의 포인트** : `+ {earnings}P`")
    users[str(user.id)]["point"] += earnings
    with open("point.json", "w") as f:
        json.dump(users, f)


async def update_bank(user, change=0, mode="point"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("point.json", "w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["point"]]
    return user


async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["point"] = 0
        users[str(user.id)]["cc_amt"] = 0
    with open("point.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("point.json", "r") as f:
        users = json.load(f)
    return users


# 서버 정보
@bot.command()
async def 서버정보(ctx):
    user_embed = discord.Embed(colour=magenta, title="<:Stella_Icon:854714421977022495> 서버 정보")
    member_count = ctx.guild.member_count
    user_embed.add_field(name=':construction_worker: 서버 주인 :', value=f"{ctx.guild.owner.name}", inline=False)
    user_embed.add_field(name=':grinning: 서버 유저수 :', value=f"{member_count}", inline=False)
    user_embed.set_footer(text='Stella Bot#9903',
                          icon_url="https://cdn.discordapp.com/avatars/806729801086926869/6d3c0df30e9a81cddf3622e630978b0c.png")

    await ctx.send(embed=user_embed)


# 공지 기능 (지금 공지 올릴때 띄어쓰기 하면 뒤에 짤림 수정 바람 Lynn_))
@bot.command()
@commands.has_permissions(administrator=True)
async def 공지(ctx, *, args):
    channel = bot.get_channel(822368253119561772)

    manager = ctx.author.name

    alarm_contents = args

    alarm = discord.Embed(colour=green, title="<:Stella_Icon:854714421977022495>**Stella 공지!**")
    alarm.add_field(name='공지 내용', value=f'{alarm_contents}')
    alarm.set_footer(text=f'처리자 : {manager}',
                     icon_url='https://cdn.discordapp.com/attachments/796274831879307265/821611491241361418/check_box.png')

    await channel.send(embed=alarm)


@bot.command()
@commands.has_permissions(administrator=True)
async def linux(ctx, *, args):
    # 윈도우일 경우 cls로 대체
    os.system('clear')
    output = subprocess.check_output(args, shell=True);
    await ctx.send("```" + output.decode('utf-8') + "```")


@bot.event
async def on_member_join(member):
    auth = bot.get_channel(822372594102566942)
    await auth.send(member.mention + "\n" + """<#777149133722091540> 에서 **인증을** 하지 않을 시에는
<:Stella_Icon:854714421977022495> Stella 서버 활동이 힘들 수 있습니다

인증 양식이 DM으로 전송 되었습니다!""")

    await member.send("\n" + """<:line:805656688362520617><:line:805656688362520617><:line:805656688362520617><:line:805656688362520617><:line:805656688362520617>***[***<:Stella_Icon:854714421977022495>***Stella 인증 시스템]***<:line:805656688362520617><:line:805656688362520617><:line:805656688362520617><:line:805656688362520617><:line:805656688362520617>
<:lunar:805653914472546312> 원활하게 Stella 커뮤니티를 이용하시려면 인증을 완료해야합니다!
<:lunar:805653914472546312> 인증은 밑에 게시된 양식을 그대로 복사하여 제출 하시는것을 권장드립니다!

**Stella 인증 양식**
```md
* 이름 :

* 현재 재학중인 학교 :

* 학년 / 번호 :

# 초대한 사람 :

[* 가 붙은 항목은 필수 제출입니다][!]
[거짓 정보 제출시에는 처벌 가능성이 있습니다][!]
```

<:check_box:824447802477772820> 처리자 : @DO_S#0313 / @Dos0313 (Sub)#4725""")


# ex 처리 / CommandError MissingRequiredArgument BadArgument CommandNotFound CommandOnCooldown
@bot.event
async def on_command_error(ctx, error):  # 예외 처리 싫으시면 pass 치시던가요
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(colour=red)
        embed.add_field(name='<:Stella_Icon:854714421977022495>에러! 필요한 값이 없음', value="필요한 인자가 없습니다!")  # 이거 좀 수정해주셈
        embed.set_footer(text='Stella Bot#9903',
                         icon_url="https://cdn.discordapp.com/avatars/806729801086926869/6d3c0df30e9a81cddf3622e630978b0c.png")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(colour=red)
        embed.add_field(name='<:Stella_Icon:854714421977022495>에러! 잘못된 값', value="인자의 값이 잘못되었습니다!")
        embed.set_footer(text='Stella Bot#9903',
                         icon_url="https://cdn.discordapp.com/avatars/806729801086926869/6d3c0df30e9a81cddf3622e630978b0c.png")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(colour=red)
        embed.add_field(name='<:Stella_Icon:854714421977022495>존재하지 않는 명령어!', value="존재하지 않는 명령어입니다!")
        embed.set_footer(text='Stella Bot#9903',
                         icon_url="https://cdn.discordapp.com/avatars/806729801086926869/6d3c0df30e9a81cddf3622e630978b0c.png")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(colour=red)
        a = error.retry_after
        after = round(a, 2)
        embed.add_field(name='<:Stella_Icon:854714421977022495>ON COOLDOWN!', value=f"**침 착 해**```남은 시간: {after}초```")
        embed.set_thumbnail(url="https://i.pinimg.com/originals/72/b7/2f/72b72ff0c392a16c6b12e80bbe3473c5.gif")
        embed.set_footer(text='Stella Bot#9903',
                         icon_url="https://cdn.discordapp.com/avatars/806729801086926869/6d3c0df30e9a81cddf3622e630978b0c.png")
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(colour=red)
        embed.add_field(name='<:Stella_Icon:854714421977022495>권한 부족!', value="이 명령어를 실행하기에는 권한이 부족합니다!")
        embed.set_footer(text='Stella Bot#9903',
                         icon_url="https://cdn.discordapp.com/avatars/806729801086926869/6d3c0df30e9a81cddf3622e630978b0c.png")
        await ctx.send(embed=embed)

    else:
        embed = discord.Embed(colour=red)
        embed.add_field(name='<:Stella_Icon:854714421977022495>알 수 없는 에러!',
                        value=f"명령어 오류 발생! 개발자한테 DM ```{str(error)}```")
        embed.set_footer(text='Stella Bot#9903',
                         icon_url="https://cdn.discordapp.com/avatars/806729801086926869/6d3c0df30e9a81cddf3622e630978b0c.png")
        await ctx.send(embed=embed)

acces_token = os.environ["BOT_TOKEN"]
bot.run(acces_token)
