from ..libs.oclib import *
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import nextcord
from config import *


class MangaSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_manga(self, manga_name: str):
        url1 = f"https://api.jikan.moe/v4/manga?q={manga_name}&limit=1"
        url2 = f"https://api.jikan.moe/v4/manga/{manga_name}"

        try:
            data = await request(url2)
            if data and data.get("data"):
                return data["data"]

            data = await request(url1)
            if data and data.get("data"):
                return data["data"][0]

        except Exception as e:
            raise e

    @commands.command(
        help="Fetch anime information from MyAnimeList. \nUsage: `manga Lycoris Recoil` or `anime 135455`.",
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def manga(self, ctx: commands.Context, *, manga_name: str):
        url = f"https://api.jikan.moe/v4/manga?q={manga_name}&limit=1"
        try:
            manga = await self.fetch_manga(manga_name)
            if manga:
                title = manga.get("title")
                chapters = manga.get("chapters")
                volumes = manga.get("volumes")
                score = manga.get("score")
                published = manga.get("published", {}).get("string")
                english_title = manga.get("title_english")
                status = manga.get("status")
                cover_image = manga["images"]["jpg"]["image_url"]
                url = manga.get("url")
                mal_id = manga.get("mal_id")
                genres = ", ".join([genre["name"] for genre in manga.get("genres", [])])
                authors = " & ".join(
                    [author["name"] for author in manga.get("authors", [])]
                )

                embed = nextcord.Embed(title=title, url=url, color=EMBED_COLOR)
                embed.description = ""
                if english_title and english_title != title:
                    embed.description += f"-# {english_title}\n"
                if status != "Publishing":
                    embed.description += f"\n> **Chapters**: {chapters}"
                    embed.description += f"\n> **Volumes**: {volumes}"
                embed.description += f"\n> **Score**: {score}"
                embed.description += f"\n> **Status**: {status}"
                embed.description += f"\n> **Genres**: {genres}"
                embed.description += f"\n> **Published**: {published}"
                embed.description += f"\n> **Authors**: {authors}"
                embed.set_thumbnail(url=cover_image)
                embed.set_footer(text=str(mal_id))

            else:
                embed = nextcord.Embed(
                    description=":x: Manga not found.",
                    color=ERROR_COLOR,
                )

        except Exception as e:
            embed = nextcord.Embed(description=str(e), color=ERROR_COLOR)
        await ctx.reply(embed=embed, mention_author=False)

    @nextcord.slash_command(
        name="manga", description="Fetch manga information from MyAnimeList."
    )
    async def slash_manga(
        self,
        interaction: Interaction,
        manga_name: str = SlashOption(description="Name of the manga"),
    ):
        url = f"https://api.jikan.moe/v4/manga?q={manga_name}&limit=1"
        try:
            manga = await self.fetch_manga(manga_name)
            if manga:
                title = manga.get("title")
                chapters = manga.get("chapters")
                volumes = manga.get("volumes")
                score = manga.get("score")
                published = manga.get("published", {}).get("string")
                english_title = manga.get("title_english")
                status = manga.get("status")
                cover_image = manga["images"]["jpg"]["image_url"]
                url = manga.get("url")
                mal_id = manga.get("mal_id")
                genres = ", ".join([genre["name"] for genre in manga.get("genres", [])])
                authors = " & ".join(
                    [author["name"] for author in manga.get("authors", [])]
                )

                embed = nextcord.Embed(title=title, url=url, color=EMBED_COLOR)
                embed.description = ""
                if english_title and english_title != title:
                    embed.description += f"-# {english_title}\n"
                if status != "Publishing":
                    embed.description += f"\n> **Chapters**: {chapters}"
                    embed.description += f"\n> **Volumes**: {volumes}"
                embed.description += f"\n> **Score**: {score}"
                embed.description += f"\n> **Status**: {status}"
                embed.description += f"\n> **Genres**: {genres}"
                embed.description += f"\n> **Published**: {published}"
                embed.description += f"\n> **Authors**: {authors}"
                embed.set_thumbnail(url=cover_image)
                embed.set_footer(text=str(mal_id))

            else:
                embed = nextcord.Embed(
                    description=":x: Manga not found.",
                    color=ERROR_COLOR,
                )

        except Exception as e:
            embed = nextcord.Embed(description=str(e), color=ERROR_COLOR)
        await interaction.response.send_message(embed=embed)


class MangaSynopsis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_manga(self, manga_name: str):
        url1 = f"https://api.jikan.moe/v4/manga?q={manga_name}&limit=1"
        url2 = f"https://api.jikan.moe/v4/manga/{manga_name}"

        try:
            data = await request(url2)
            if data and data.get("data"):
                return data["data"]

            data = await request(url1)
            if data and data.get("data"):
                return data["data"][0]

        except Exception as e:
            raise e

    @commands.command(
        aliases=["mangaplot", "mangasyn"],
        help="Fetch anime information from MyAnimeList. \nUsage: `mangasyn Lycoris Recoil` or `mangasyn 50709`.",
    )
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def manga_synopsis(self, ctx: commands.Context, *, manga_name: str):
        url = f"https://api.jikan.moe/v4/manga?q={manga_name}&limit=1"
        try:
            manga = await self.fetch_manga(manga_name)
            if manga:
                title = manga.get("title")
                english_title = manga.get("title_english")
                cover_image = manga["images"]["jpg"]["image_url"]
                url = manga.get("url")
                mal_id = manga.get("mal_id")
                synopsis = manga.get("synopsis")
                if len(synopsis) > 700:
                    synopsis = synopsis[:700] + "..."

                embed = nextcord.Embed(title=title, url=url, color=EMBED_COLOR)
                embed.description = ""
                if english_title and english_title != title:
                    embed.description += f"-# {english_title}\n"
                embed.description += f"\n{synopsis}"
                embed.set_thumbnail(url=cover_image)
                embed.set_footer(text=str(mal_id))

            else:
                embed = nextcord.Embed(
                    description=":x: Manga not found.",
                    color=ERROR_COLOR,
                )

        except Exception as e:
            embed = nextcord.Embed(description=str(e), color=ERROR_COLOR)
        await ctx.reply(embed=embed, mention_author=False)

    @nextcord.slash_command(
        name="manga_synopsis", description="Fetch manga synopsis from MyAnimeList."
    )
    async def slash_manga_synopsis(
        self,
        interaction: Interaction,
        manga_name: str = SlashOption(description="Name of the manga"),
    ):
        url = f"https://api.jikan.moe/v4/manga?q={manga_name}&limit=1"
        try:
            manga = await self.fetch_manga(manga_name)
            if manga:
                title = manga.get("title")
                english_title = manga.get("title_english")
                cover_image = manga["images"]["jpg"]["image_url"]
                url = manga.get("url")
                mal_id = manga.get("mal_id")
                synopsis = manga.get("synopsis")
                if len(synopsis) > 700:
                    synopsis = synopsis[:700] + "..."

                embed = nextcord.Embed(title=title, url=url, color=EMBED_COLOR)
                embed.description = ""
                if english_title and english_title != title:
                    embed.description += f"-# {english_title}\n"
                embed.description += f"\n{synopsis}"
                embed.set_thumbnail(url=cover_image)
                embed.set_footer(text=str(mal_id))

            else:
                embed = nextcord.Embed(
                    description=":x: Manga not found.",
                    color=ERROR_COLOR,
                )

        except Exception as e:
            embed = nextcord.Embed(description=str(e), color=ERROR_COLOR)
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(MangaSearch(bot))
    bot.add_cog(MangaSynopsis(bot))
