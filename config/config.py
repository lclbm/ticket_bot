import json
from pathlib import Path
from pydantic import BaseModel


class GuildConfig(BaseModel):
    guild_id: str  #服务器的guild_id
    super_user_ids: list[str]
    menu_channel_ids: list[str]  # 该把发起帮助的消息卡片发送到哪几个频道
    help_category_id: str  # 需要创建帮助文字频道的分组id
    helper_role_ids: list[str]  # 帮助他人的角色ids


class BotConfig(BaseModel):
    token: str
    super_user_ids: list[str]
    guild_config: dict[str, GuildConfig]


class Config:
    __loaded: bool = False
    __config_path: Path = Path(".") / "config.json"

    token: str  # 机器人的token
    super_user_ids: list[str]  # bot管理员的id
    guild_config: dict[str, GuildConfig] = {}

    @classmethod
    def load(cls):
        bot_config = BotConfig.parse_file(cls.__config_path)
        cls.token = bot_config.token
        cls.super_user_ids = bot_config.super_user_ids
        cls.guild_config = bot_config.guild_config
        cls.__loaded = True
