from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import PubSubData

__all__ = [
    'PubSubModerationAction'
]


class PubSubModerationAction:
    def __init__(self, raw: 'PubSubData'):
        self.data = raw

    @property
    def topic(self) -> str:
        return self.data.topic

    @property
    def message_data_type(self) -> str:
        return self.data.message_data.get('type', '')

    @property
    def moderation_action(self) -> str:
        return self.data.moderation_action

    @property
    def args(self) -> list:
        return self.data.args

    @property
    def created_by(self) -> str:
        return self.data.created_by

    @property
    def created_by_user_id(self) -> str:
        return self.data.created_by_user_id

    @property
    def msg_id(self) -> str:
        return self.data.msg_id

    @property
    def target_user_id(self) -> str:
        return self.data.target_user_id

    @property
    def target_user_login(self) -> str:
        return self.data.target_user_login

    @property
    def from_automod(self) -> bool:
        return self.data.from_automod
