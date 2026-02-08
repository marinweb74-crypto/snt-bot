from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


BACK_BTN = InlineKeyboardButton(text="<< Назад", callback_data="back")


def _add_back(buttons: list[list[InlineKeyboardButton]], show_back: bool):
    if show_back:
        buttons.append([BACK_BTN])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_q1_role(show_back=False) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Председатель", callback_data="role:chairman")],
        [InlineKeyboardButton(text="Член Правления", callback_data="role:board_member")],
        [InlineKeyboardButton(text="Бухгалтер", callback_data="role:accountant")],
    ]
    return _add_back(buttons, show_back)


def kb_yes_no(prefix: str, show_back=True) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Да", callback_data=f"{prefix}:yes"),
            InlineKeyboardButton(text="Нет", callback_data=f"{prefix}:no"),
        ],
    ]
    return _add_back(buttons, show_back)


def kb_q5_debt_period(show_back=True) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="1 год", callback_data="period:1year")],
        [InlineKeyboardButton(text="3 года", callback_data="period:3years")],
        [InlineKeyboardButton(text="Больше", callback_data="period:more")],
    ]
    return _add_back(buttons, show_back)


def kb_q6_debt_amount(show_back=True) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="До 50 000 руб.", callback_data="amount:50k")],
        [InlineKeyboardButton(text="До 100 000 руб.", callback_data="amount:100k")],
        [InlineKeyboardButton(text="Свыше 100 000 руб.", callback_data="amount:above100k")],
    ]
    return _add_back(buttons, show_back)


def kb_q7_actions(selected: list[str], show_back=True) -> InlineKeyboardMarkup:
    options = [
        ("Устные просьбы", "act:oral"),
        ("Письма-претензии по e-mail", "act:email"),
        ("Досудебные претензии", "act:pretrial"),
        ("Иное", "act:other"),
    ]
    buttons = []
    for text, data in options:
        check = "\u2705 " if data in selected else ""
        buttons.append([InlineKeyboardButton(text=f"{check}{text}", callback_data=data)])
    buttons.append([InlineKeyboardButton(text="Готово \u00bb", callback_data="act:done")])
    return _add_back(buttons, show_back)


def kb_q9_debtor_data(selected: list[str], show_back=True) -> InlineKeyboardMarkup:
    options = [
        ("Кадастровый номер участка", "data:cadastral"),
        ("Паспортные данные", "data:passport"),
        ("Место проживания", "data:address"),
        ("Телефон должника", "data:phone"),
        ("Адрес эл. почты", "data:email"),
        ("ИНН", "data:inn"),
    ]
    buttons = []
    for text, data in options:
        check = "\u2705 " if data in selected else ""
        buttons.append([InlineKeyboardButton(text=f"{check}{text}", callback_data=data)])
    buttons.append([InlineKeyboardButton(text="Готово \u00bb", callback_data="data:done")])
    return _add_back(buttons, show_back)


def kb_confirm_another() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да, заполнить ещё", callback_data="another:yes"),
            InlineKeyboardButton(text="Нет, спасибо", callback_data="another:no"),
        ],
    ])
