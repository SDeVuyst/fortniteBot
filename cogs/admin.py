""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 5.5.0
"""

import discord
import os
import embeds
import random
import asyncio

import random
from discord import app_commands
from discord.ext import commands
from helpers import ArtBuilder, checks, db_manager
from discord.ext.commands import has_permissions
from datetime import datetime
from exceptions import CogLoadError
from discord.ext.commands import has_permissions
from datetime import datetime



class Admin(commands.Cog, name="admin"):
    def __init__(self, bot):
        self.bot = bot

    conmand_cog_group = app_commands.Group(name="cog", description="Cog Group")
    blacklist_group = app_commands.Group(name="blacklist", description="Blacklist Group")


    @app_commands.command(
        name="sync",
        description="Synchronizes the slash commands (admin only)",
        extras={'cog': 'admin'}
    )
    @app_commands.describe(scope="The scope of the sync.")
    @app_commands.choices(scope=[
        discord.app_commands.Choice(name="Global", value="global"),
        discord.app_commands.Choice(name="Server", value="server"),
    ])
    @checks.is_owner()
    async def sync(self, interaction, scope: discord.app_commands.Choice[str]) -> None:
        """Synchronizes the slash commands

        Args:
            interaction (Interaction): Users interaction
            scope (discord.app_commands.Choice[str]): The scope to sync, can be global or server
        """
        await interaction.response.defer()

        if scope.value == "global":
            cmds = await self.bot.tree.sync()
            self.bot.save_ids(cmds)

            return await interaction.followup.send(embed=embeds.OperationSucceededEmbed(
                "Slash commands have been globally synchronized."
            ))

        elif scope.value == "server":

            # context.bot.tree.copy_global_to(guild=context.guild)
            cmds = await self.bot.tree.sync(guild=interaction.guild)
            self.bot.save_ids(cmds)

            return await interaction.followup.send(embed=embeds.OperationSucceededEmbed(
                "Slash commands have been synchronized in this server."
            ))
            

        await interaction.followup.send(embed=embeds.OperationFailedEmbed(
            "The scope must be 'global' or 'server'"
        ))



    @conmand_cog_group.command(
        name="load",
        description="Load a cog (admin only)",
        extras={'cog': 'admin', 'prefix': 'cog'}
    )
    @app_commands.describe(cog="The name of the cog to load")
    @checks.is_owner()
    async def load_cog(self, interaction, cog: str) -> None:
        """Load a given cog

        Args:
            interaction (Interaction): users interaction
            cog (str): The cog to load
        """
        try:
            await self.bot.load_extension(f"cogs.{cog}")
            self.bot.loaded.add(cog)
            self.bot.unloaded.discard(cog)

        except Exception:
            raise CogLoadError(cog, 0)

        await interaction.response.send_message(embed=embeds.OperationSucceededEmbed(
            f"Successfully loaded the `{cog}` cog."
        ))



    @conmand_cog_group.command(
        name="unload",
        description="Unloads a cog (admin only)",
        extras={'cog': 'admin', 'prefix': 'cog'}
    )
    @app_commands.describe(cog="The name of the cog to unload")
    @checks.is_owner()
    async def unload_cog(self, interaction, cog: str) -> None:
        """Unloads a cog

        Args:
            interaction (Interaction): Users Interaction
            cog (str): The cog to unload
        """
        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            self.bot.loaded.discard(cog)
            self.bot.unloaded.add(cog)
        except Exception:
            raise CogLoadError(cog, 1)

        await interaction.response.send_message(embed=embeds.OperationSucceededEmbed(
            f"Successfully unloaded the `{cog}` cog."
        ))



    @conmand_cog_group.command(
        name="reload",
        description="Reloads a cog (admin only)",
        extras={'cog': 'admin', 'prefix': 'cog'}
    )
    @app_commands.describe(cog="The name of the cog to reload")
    @checks.is_owner()
    async def reload_cog(self, interaction, cog: str) -> None:
        """Reloads a cog

        Args:
            interaction (Interaction): Users interaction
            cog (str): The cog to reload
        """
        try:
            await self.bot.reload_extension(f"cogs.{cog}")

        except Exception:
            raise CogLoadError(cog, 2)

        await interaction.response.send_message(embed=embeds.OperationSucceededEmbed(
            f"Successfully reloaded the `{cog}` cog."
        ))


    @conmand_cog_group.command(
        name="all",
        description="See loaded/unloaded cogs (admin only)",
        extras={'cog': 'admin', 'prefix': 'cog'}
    )
    @checks.is_owner()
    async def all(self, interaction) -> None:
        """Shows which cogs are loaded/unloaded

        Args:
            interaction (Interaction): users interaction
        """
        embed = embeds.DefaultEmbed(
            "Cog Info"
        )
        loaded_fields = "\n".join(list(self.bot.loaded))
        embed.add_field(
            name="Loaded", value=f'```\n{loaded_fields}```', inline=False
        )

        unloaded_fields = "\n".join(list(self.bot.unloaded))
        if len(unloaded_fields) > 0:
            embed.add_field(
                name="Unloaded", value=f"```\n{unloaded_fields}```", inline=False
            )

        await interaction.response.send_message(embed=embed)


    @app_commands.command(
        name="restart",
        description="Make the bot restart (admin only)",
        extras={'cog': 'admin'}
    )
    @checks.is_owner()
    async def restart(self, interaction) -> None:
        """Restarts the bot

        Args:
            interaction (Interaction): Users Interaction
        """
        await interaction.response.send_message(embed=embeds.DefaultEmbed(
            "Restarting. brb :wave:"
        ))

        # We shut down the bot, but heroku will automatically restart it.
        await self.bot.close()



async def setup(bot):
    await bot.add_cog(Admin(bot))

