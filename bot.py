import asyncio
from khl import (
    Bot,
    PublicMessage,
    Message,
    Channel,
    PublicTextChannel,
    EventTypes,
    Event,
    ChannelTypes,
)
from config import Config
from utils import WELCOME_CARD_MESSAGE
from khl.card import CardMessage, Card, Module, Element, Types

bot = Bot(Config.token)


def is_guild_marked():
    async def rule(msg: Message) -> bool:
        return msg.guild.id in Config.guild_config

    return rule


def is_super_user_message():
    async def rule(msg: Message) -> bool:
        return msg.author_id in Config.super_user_ids or (
            msg.guild.id in Config.guild_config
            and msg.author_id in Config.guild_config[msg.guild.id].super_user_ids
        )

    return rule


def is_in_helping_channel():
    async def rule(msg: Message) -> bool:
        if msg.guild.id not in Config.guild_config:
            return False
        await msg.ctx.guild.load()
        channels = [
            i["id"]
            for i in msg.guild.channels
            if i["parent_id"] == Config.guild_config[msg.guild.id].help_category_id
        ]
        return msg.ctx.channel.id in channels

    return rule


@bot.command(regex="^发送ticket菜单$", rules=[is_guild_marked(), is_super_user_message()])
async def send_menu(message: Message, bot: Bot):

    await asyncio.gather(
        *[
            bot.send(
                PublicTextChannel(id=channel_id, _gate_=bot.client.gate),
                WELCOME_CARD_MESSAGE,
            )
            for channel_id in Config.guild_config[message.guild.id].menu_channel_ids
        ]
    )


@bot.command(
    regex="^关闭$",
    rules=[is_super_user_message(), is_guild_marked(), is_in_helping_channel()],
)
async def delete_channel(message: Message, bot: Bot):
    await message.guild.delete_channel(message.channel)


@bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
async def on_message_btn_click(bot: Bot, event: Event):
    value: str = event.body["value"]
    user_id: str = event.body["user_id"]
    guild_id: str = event.body["guild_id"]
    channel_id: str = event.body["target_id"]
    guild = await bot.fetch_guild(guild_id)
    channel = await bot.fetch_public_channel(channel_id)
    user = await guild.fetch_user(user_id)

    match value:
        case "发起ticket":
            channel: PublicTextChannel = await guild.create_channel(
                user.nickname,
                ChannelTypes.TEXT,
                Config.guild_config[guild_id].help_category_id,
            )
            role_msg = " ".join(
                [
                    f"(rol){role_id}(rol)"
                    for role_id in Config.guild_config[guild_id].helper_role_ids
                ]
            )
            content = f'(met){user_id}(met)发起了帮助，请等待管理员的回复\n{role_msg}\n帮助结束后点击下方"关闭"按钮即可关闭该ticket频道'
            await channel.send(
                CardMessage(
                    Card(
                        Module.Section(Element.Text(content, Types.Text.KMD)),
                        Module.ActionGroup(
                            Element.Button("关闭", "关闭ticket", theme=Types.Theme.DANGER)
                        ),
                    )
                )
            )
            await channel.update_permission(user, 6144)
        case "关闭ticket":
            await guild.delete_channel(channel)


bot.run()
