import nextcord
from nextcord.ext import application_checks, commands
from ..libs.oclib import *
from config import *


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(
        name="role",
        description="Base role command, if no subcommand is passed.",
        invoke_without_command=True,
    )
    async def role(self, ctx: commands.Context):
        embed = nextcord.Embed(
            description="Please specify a subcommand: `add` or `remove`",
            color=EMBED_COLOR,
        )
        await ctx.reply(embed=embed, mention_author=False)

    @role.command(
        name="add",
        help="Add a role to a member. \nUsage: `role add <role> <member>`.",
    )
    @commands.has_permissions(manage_roles=True)
    async def add(self, ctx: commands.Context, role: nextcord.Role, member: str = None):
        if member is None:
            member = ctx.author
        else:
            member = extract_user_id(member, ctx)
            if isinstance(member, nextcord.Embed):
                await ctx.reply(embed=member, mention_author=False)
                return

        await member.add_roles(role, reason=f"Role added by {ctx.author}")
        embed = nextcord.Embed(
            description=f"✅ Added role {role.mention} to {member.mention}.",
            color=EMBED_COLOR,
        )
        await ctx.reply(embed=embed, mention_author=False)

    @role.command(
        name="remove",
        help="Remove a role from member. \nUsage: `role remove <role> <member>`.",
    )
    @commands.has_permissions(manage_roles=True)
    async def remove(
        self, ctx: commands.Context, role: nextcord.Role, member: str = None
    ):
        if member is None:
            member = ctx.author
        else:
            member = extract_user_id(member, ctx)
            if isinstance(member, nextcord.Embed):
                await ctx.reply(embed=member, mention_author=False)
                return

        await member.remove_roles(role, reason=f"Role removed by {ctx.author}")
        embed = nextcord.Embed(
            description=f"✅ Removed role {role.mention} from {member.mention}.",
            color=EMBED_COLOR,
        )
        await ctx.reply(embed=embed, mention_author=False)


class RolesSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @nextcord.slash_command(name="role", description="Role management commands.")
    async def role(self, interaction: nextcord.Interaction):
        pass

    @role.subcommand(name="add", description="Add a role to a member.")
    @application_checks.has_permissions(manage_roles=True)
    async def add(
        self,
        interaction: nextcord.Interaction,
        role: nextcord.Role = nextcord.SlashOption(
            description="The role to add", required=True
        ),
        member: nextcord.Member = nextcord.SlashOption(
            description="The member to add the role to", required=True
        ),
    ):

        await member.add_roles(role, reason=f"Role added by {interaction.user}")
        embed = nextcord.Embed(
            description=f"✅ Added role {role.mention} to {member.mention}.",
            color=EMBED_COLOR,
        )
        await interaction.send(embed=embed)

    @role.subcommand(name="remove", description="Remove a role from member.")
    @application_checks.has_permissions(manage_roles=True)
    async def remove(
        self,
        interaction: nextcord.Interaction,
        role: nextcord.Role = nextcord.SlashOption(
            description="The role to remove", required=True
        ),
        member: nextcord.Member = nextcord.SlashOption(
            description="The member to remove the role from", required=True
        ),
    ):

        await member.remove_roles(role, reason=f"Role removed by {interaction.user}")
        embed = nextcord.Embed(
            description=f"✅ Removed role {role.mention} from {member.mention}.",
            color=EMBED_COLOR,
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Roles(bot))
    bot.add_cog(RolesSlash(bot))
