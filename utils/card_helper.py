from khl.card import CardMessage, Card, Module, Element, Types

WELCOME_CARD_MESSAGE: CardMessage


def init_welcome_card_message():
    global WELCOME_CARD_MESSAGE
    WELCOME_CARD_MESSAGE = CardMessage(
        Card(
            Module.Section(
                "点击右侧按钮发起ticket",
                Element.Button("发起ticket", "发起ticket"),
                Types.SectionMode.RIGHT,
            )
        )
    )


init_welcome_card_message()
