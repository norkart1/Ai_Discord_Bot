import nextcord
from nextcord.ext import application_checks, commands
from nextcord import Interaction, SlashOption
from motor.motor_asyncio import AsyncIOMotorClient
from config import *
from ..libs.oclib import *


class Reports(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = AsyncIOMotorClient(MONGO_URI).get_database(DB_NAME)

    async def get_server_config(self, guild_id: int):
        """Retrieve the report settings for a server from the database."""
        return await self.db.report_settings.find_one({"guild_id": guild_id})

    async def set_server_config(
        self, guild_id: int, mod_role_id: int, reports_channel_id: int
    ):
        """Set or update the report settings for a server."""
        await self.db.report_settings.update_one(
            {"guild_id": guild_id},
            {
                "$set": {
                    "moderator_role_id": mod_role_id,
                    "reports_channel_id": reports_channel_id,
                }
            },
            upsert=True,
        )

    @nextcord.slash_command(
        name="report",
        description="Report something to server's moderation team.",
    )
    async def report(
        self,
        interaction: Interaction,
        user: nextcord.Member = SlashOption(
            description="User being reported.", required=True
        ),
        reason: str = SlashOption(description="Reason for the report."),
        channel: nextcord.TextChannel = SlashOption(
            description="The channel where the incident occured.", required=False
        ),
    ):
        guild_id = interaction.guild.id
        config = await self.get_server_config(guild_id)

        if not config:
            await interaction.response.send_message(
                "Reports system is not set up. Please contact an admin.", ephemeral=True
            )
            return

        moderator_role_id = config.get("moderator_role_id")
        reports_channel_id = config.get("reports_channel_id")

        reports_channel = self.bot.get_channel(reports_channel_id)
        if not reports_channel:
            await interaction.response.send_message(
                "Reports channel not found.", ephemeral=True
            )
            return

        embed = nextcord.Embed(
            title="New Report",
            description=f"Issue reported in {interaction.channel.mention}",
            color=ERROR_COLOR,
        )
        embed.add_field(name="Reason", value=reason, inline=False)

        embed.add_field(name="Reported User", value=user.mention, inline=False)
        if user.avatar:
            embed.set_thumbnail(url=user.avatar.url)

        embed.set_footer(
            text=f"Reported by {interaction.user}",
            icon_url=interaction.user.display_avatar.url,
        )

        # Send the embed to the reports channel, pinging the moderator role
        await reports_channel.send(
            content=f"<@&{moderator_role_id}>",
            embed=embed,
            allowed_mentions=nextcord.AllowedMentions(roles=True),
        )
        submitted_embed = nextcord.Embed(
            description=f"✅ Report successfully submitted. Thank you for helping to keep our server safe!",
            color=nextcord.Color.green(),
        )
        await interaction.response.send_message(embed=submitted_embed, ephemeral=True)

    @nextcord.slash_command(
        name="admin_report", description="Set up the report system for this server."
    )
    @application_checks.has_permissions(administrator=True)
    async def admin_report(
        self,
        interaction: Interaction,
        mod_role: nextcord.Role = SlashOption(
            description="The moderator role to ping."
        ),
        reports_channel: nextcord.TextChannel = SlashOption(
            description="The channel where reports will be sent."
        ),
    ):
        guild_id = interaction.guild.id

        await self.set_server_config(guild_id, mod_role.id, reports_channel.id)

        await interaction.response.send_message(
            f"Successfully set up the report system. Moderator role: {mod_role.mention}, reports channel: {reports_channel.mention}",
            ephemeral=True,
        )


def setup(bot):
    bot.add_cog(Reports(bot))
