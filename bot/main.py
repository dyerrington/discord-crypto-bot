import discord
from discord.ext import tasks

# data libraries
import pandas as pd
from lunarcrush import LunarCrush

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)
        self.printer.start()

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')


    def get_coin(self, symbol = "ZIL"):
        lc = LunarCrush()
        coin = lc.get_assets(symbol=['ZIL'], data_points=2, interval='1h')

        coin_historical         = pd.DataFrame(coin['data'][0]['timeSeries'])
        coin_historical['date'] = pd.to_datetime(coin_historical.time, unit = "s")
        coin_historical         = coin_historical.set_index('date')

        return coin, coin_historical

    def get_embed(self, coin, df, pct):
 
        embed = discord.Embed(
            title       =   coin['data'][0]['name'],
            url         =   f"https://coinmarketcap.com/currencies/{coin['data'][0]['name'].lower()}/",
            description =   f"❗ Alert - 1 Hour PCT ({pct}%) ❗",
            color       =   discord.Color.blue()
        )

        pct_1h = df.pct_change(periods = 1, fill_method = "ffill")['close'].iloc[1].round(3) * 100

        # embed.set_author(name="RealDrewData", url="https://twitter.com/RealDrewData", icon_url="https://cdn-images-1.medium.com/fit/c/32/32/1*QVYjh50XJuOLQBeH_RZoGw.jpeg")
        # embed.set_author(name=ctx.author.display_name, url="https://twitter.com/RealDrewData", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
        embed.add_field(name="**symbol**",             value = coin['data'][0]['symbol'], inline=False)
        embed.add_field(name="**price**",              value = coin['data'][0]['price'], inline=False)
        embed.add_field(name="**market_cap**",         value = coin['data'][0]['market_cap'], inline=False)
        embed.add_field(name="**percept_change_1h**",  value = pct_1h, inline=False)
        embed.add_field(name="**percent_change_24h**", value = coin['data'][0]['percent_change_24h'], inline=False)
        embed.add_field(name="**percent_change_7d**",  value = coin['data'][0]['percent_change_7d'], inline=False)
        embed.add_field(name="**percent_change_30d**", value = coin['data'][0]['percent_change_30d'], inline=False)
        embed.add_field(name="**volume_24h**",         value = coin['data'][0]['volume_24h'], inline=False)
        embed.add_field(name="**max_supply**",         value = coin['data'][0]['max_supply'], inline=False)

        # embed.add_field(name="*Italics*", value="Surround your text in asterisks (\*)", inline=False)
        # embed.add_field(name="**Bold**", value="Surround your text in double asterisks (\*\*)", inline=False)
        # embed.add_field(name="__Underline__", value="Surround your text in double underscores (\_\_)", inline=False)
        # embed.add_field(name="~~Strikethrough~~", value="Surround your text in double tildes (\~\~)", inline=False)
        # embed.add_field(name="`Code Chunks`", value="Surround your text in backticks (\`)", inline=False)
        # embed.add_field(name="Blockquotes", value="> Start your text with a greater than symbol (\>)", inline=False)
        # embed.add_field(name="Secrets", value="||Surround your text with double pipes (\|\|)||", inline=False)
        embed.set_footer(text="Provided by: coinmarketcap.com")
        return embed

    ## This is a loop where notifications can be sent
    @tasks.loop(seconds=3600.0)
    async def printer(self):
        for server in self.guilds:
            for channel in server.text_channels:

                if 'cryptobismo' in channel.name:

                    coin, df  = self.get_coin('BTC')
                    embed     = self.get_embed(coin, df, "3")

                    pct_change = df.pct_change(periods = 1, fill_method = "ffill")['close'].iloc[1].round(3)
                    print(f"BTC PCT % is {pct_change}")

                    if abs(pct_change) >= .2: 
        
                        print("SEnding message to ", channel.name)
                        await channel.send(embed = embed)

                if 'experiment' in channel.name:

                    coin, df  = self.get_coin('ZIL')
                    embed     = self.get_embed(coin, df, "5")

                    pct_change = df.pct_change(periods = 1, fill_method = "ffill")['close'].iloc[1].round(3)
                    print(f"ZIL PCT % is {pct_change}")

                    if abs(pct_change) >= .5: 
        
                        print("SEnding message to ", channel.name)
                        await channel.send(embed = embed)
                    
                    # print("Shit is getting ready...", type(channel), dir(channel))

client = MyClient()
client.run('OTU3NDA3Mjc3MTg5NTc4ODEz.Yj-VAg.WDPrx1utgHt_9DtXMXYVHs6AyO8') # this token is not valid -- issue yourself one 
from Discord
