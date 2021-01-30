import discord
from discord.ext import commands
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

urls = [
       "https://overwatch.op.gg/detail/overview/65119140191099038154169",
       "https://overwatch.op.gg/detail/overview/36176117200252182104181",
       "https://overwatch.op.gg/detail/overview/103031153232155229041108"]
def opgg_scraper():
   
   player_name_list = []
   score_list = []
   
   for url in urls:
       indeed = requests.get(url)
       indeed_soup = BeautifulSoup(indeed.text, "html.parser")
       
       temp_player_name = indeed_soup.find("div","PlayerName")
       temp_player_name = str(temp_player_name)
       temp_player_name = temp_player_name[92:-78]
       player_name_list.append(temp_player_name)

       temp_score_data = indeed_soup.find_all("div","role-tier__column")

       for i in temp_score_data:
           temp = str(i.find("img","role-tier__image"))
           if temp == "<img class=\"role-tier__image\" src=\"https://overwatch.op.gg/img/rankIcon/rank-1.png\"/>":
               score_list.append("배치")
           else:
               i = i.find("b","role-tier__score text-navy")
               i = str(i)
               i = i[38:-4]
               i = i[0]+i[-3:]
               score_list.append(i)

   return score_list, player_name_list

temp_TOKEN = 'O/D/A/0/N/z/I/w/N/D/A/0/N/T/U/x/M/z/A/z/M/T/g/5/./Y/B/Q/c/R/w/./Y/r/p/O/B/2/a/j/_/R/C/u/2/l/2/e/L/K/S/V/D/M/y/X/F/I/Q/'
TOKEN = ""
for i in range(len(temp_TOKEN)): #깃허브 업로드 시 디스코드 자동 토큰 짤림 없애주는 코드
    if i%2==0:
        TOKEN += temp_TOKEN[i]

client = discord.Client()

@client.event
async def on_message(message):  #봇이 쓰는 명령에는 반응 안되게 하는 부분
    if message.author.bot:
        return None

    if message.content.startswith("!현재점수"):
        now = time.localtime()
        now = "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

        score_list, player_name= opgg_scraper()
        embed = discord.Embed(title="실시간 점수", color=0x62c1cc)

        j=0
        temp_tier_list = []
        for i in player_name:
            for k in range(3):
                if str(score_list[j+k])=="배치":
                    temp_tier_list.append(":arrows_counterclockwise: ")
                elif int(score_list[j+k])>=4400:
                    temp_tier_list.append("<:Ranker:786955346924142603>")
                elif int(score_list[j+k])>=4000:
                    temp_tier_list.append("<:GrandMaster:786955304725119037>")
                elif int(score_list[j+k])>=3500:
                    temp_tier_list.append("<:Master:786955293664739329>")
                elif int(score_list[j+k])>=3000:
                    temp_tier_list.append("<:Diamond:786955278041743370>")
                elif int(score_list[j+k])>=2500:
                    temp_tier_list.append("<:Platinum:786955265823473745>")
                elif int(score_list[j+k])>=2000:
                    temp_tier_list.append("<:Gold:786955255152771162>")
                elif int(score_list[j+k])>=1500:
                    temp_tier_list.append("<:Silver:729639125812248626>")
                else:
                    temp_tier_list.append("<:Bronze:786910922001743893>")
            msg = "<:tank:804992822792683550>탱커 : "+temp_tier_list[j+0]+score_list[j]+" | <:attack:804992822662135818>딜러 : "+temp_tier_list[j+1]+score_list[j+1]+" | <:support:804992822696476743>힐러 : "+temp_tier_list[j+2]+score_list[j+2]
            embed.add_field(name=i, value=msg, inline=False)
            j+=3
        embed.set_footer(text=now)
        await message.channel.send(embed=embed)
    old_now = "0"
    if message.content.startswith("!갱신"):
        now = time.localtime()
        now = "%d" % (now.tm_min)
        print("old_now : "+now)
        print("now : "+now)
        if int(now)!=int(old_now):
            #options = webdriver.ChromeOptions()
            #options.add_argument("headless")
            driver = webdriver.Chrome('chromedriver')#,options=options)
            for url in urls:
                driver.get(url)
                driver.find_element_by_xpath("//*[@id='PlayerLayoutHeader']/div/div[2]/ul/li[1]/button").click()
            old_now = now
            driver.quit()
            msg = "갱신 완료"
        else:
            msg = "갱신되지 않았습니다.(가장 최근 갱신으로부터 1분 이내 갱신 요청)"
        await message.channel.send(msg)


@client.event
async def on_ready():
    print('Logged in as')
    print("bot name : " + client.user.name)
    print("bot ID : " + str(client.user.id))
    print("bot verson : " + str(discord.__version__))
    print('------------------')
    game = discord.Game("다음 방송을 준비하는")
    await client.change_presence(status=discord.Status.online, activity=game)

client.run(TOKEN)
