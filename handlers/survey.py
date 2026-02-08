import re
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from states import SurveyStates
from keyboards import (
    kb_q1_role, kb_yes_no, kb_q5_debt_period, kb_q6_debt_amount,
    kb_q7_actions, kb_q9_debtor_data, kb_confirm_another,
)

router = Router()

ROLE_LABELS = {
    "role:chairman": "Председатель",
    "role:board_member": "Член Правления",
    "role:accountant": "Бухгалтер",
}

PERIOD_LABELS = {
    "period:1year": "1 год",
    "period:3years": "3 года",
    "period:more": "Больше",
}

AMOUNT_LABELS = {
    "amount:50k": "До 50 000 руб.",
    "amount:100k": "До 100 000 руб.",
    "amount:above100k": "Свыше 100 000 руб.",
}

ACTION_LABELS = {
    "act:oral": "Устные просьбы о погашении задолженности",
    "act:email": "Письма-претензии по электронной почте",
    "act:pretrial": "Досудебные претензии (заказным письмом)",
    "act:other": "Иное",
}

DATA_LABELS = {
    "data:cadastral": "Кадастровый номер участка",
    "data:passport": "Паспортные данные",
    "data:address": "Место проживания",
    "data:phone": "Телефон должника",
    "data:email": "Адрес электронной почты",
    "data:inn": "ИНН",
}


# --- Question display helpers ---

async def show_q1(message_or_cb, state: FSMContext):
    await state.set_state(SurveyStates.q1_role)
    text = "Вопрос 1 из 10\n\nКем Вы являетесь в СНТ?"
    if isinstance(message_or_cb, CallbackQuery):
        await message_or_cb.message.edit_text(text, reply_markup=kb_q1_role(show_back=False))
    else:
        await message_or_cb.answer(text, reply_markup=kb_q1_role(show_back=False))


async def show_q2(cb: CallbackQuery, state: FSMContext):
    await state.set_state(SurveyStates.q2_name)
    await cb.message.edit_text(
        "Вопрос 2 из 10\n\nКак Вас зовут?\n\nВведите ваше имя текстом:"
    )


async def show_q3(source, state: FSMContext):
    await state.set_state(SurveyStates.q3_is_member)
    text = "Вопрос 3 из 10\n\nДолжник является ли членом товарищества?"
    if isinstance(source, CallbackQuery):
        await source.message.edit_text(text, reply_markup=kb_yes_no("member"))
    else:
        await source.answer(text, reply_markup=kb_yes_no("member"))


async def show_q4(cb: CallbackQuery, state: FSMContext):
    await state.set_state(SurveyStates.q4_is_sole_owner)
    await cb.message.edit_text(
        "Вопрос 4 из 10\n\nДолжник является единственным собственником участка?",
        reply_markup=kb_yes_no("owner"),
    )


async def show_q5(cb: CallbackQuery, state: FSMContext):
    await state.set_state(SurveyStates.q5_debt_period)
    await cb.message.edit_text(
        "Вопрос 5 из 10\n\nЗа какой период сформировался долг?",
        reply_markup=kb_q5_debt_period(),
    )


async def show_q6(cb: CallbackQuery, state: FSMContext):
    await state.set_state(SurveyStates.q6_debt_amount)
    await cb.message.edit_text(
        "Вопрос 6 из 10\n\nОбщая сумма долга:",
        reply_markup=kb_q6_debt_amount(),
    )


async def show_q7(cb: CallbackQuery, state: FSMContext):
    await state.set_state(SurveyStates.q7_actions)
    data = await state.get_data()
    selected = data.get("actions_selected", [])
    await cb.message.edit_text(
        "Вопрос 7 из 10\n\nКакие действия Вы предпринимали для погашения задолженности?\n\n"
        "Выберите один или несколько вариантов, затем нажмите «Готово».",
        reply_markup=kb_q7_actions(selected),
    )


async def show_q8(source, state: FSMContext):
    await state.set_state(SurveyStates.q8_written_response)
    text = "Вопрос 8 из 10\n\nЕсть ли ответы должника в Ваш адрес в письменной форме?"
    if isinstance(source, CallbackQuery):
        await source.message.edit_text(text, reply_markup=kb_yes_no("written"))
    else:
        await source.answer(text, reply_markup=kb_yes_no("written"))


async def show_q9(cb: CallbackQuery, state: FSMContext):
    await state.set_state(SurveyStates.q9_debtor_data)
    data = await state.get_data()
    selected = data.get("debtor_data_selected", [])
    await cb.message.edit_text(
        "Вопрос 9 из 10\n\nЕсть ли у Вас данные на должника?\n\n"
        "Выберите один или несколько вариантов, затем нажмите «Готово».",
        reply_markup=kb_q9_debtor_data(selected),
    )


async def show_q10(source, state: FSMContext):
    await state.set_state(SurveyStates.q10_phone)
    text = "Вопрос 10 из 10\n\nОставьте Ваш контактный номер телефона для обратной связи.\n\nВведите номер в формате: +7XXXXXXXXXX"
    if isinstance(source, CallbackQuery):
        await source.message.edit_text(text)
    else:
        await source.answer(text)


# --- Q1: Role ---

@router.callback_query(SurveyStates.q1_role, F.data.startswith("role:"))
async def on_q1(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(role=ROLE_LABELS[cb.data])
    await show_q2(cb, state)


# --- Q2: Name (text input) ---

@router.message(SurveyStates.q2_name)
async def on_q2(message: Message, state: FSMContext):
    name = message.text.strip() if message.text else ""
    if len(name) < 2 or len(name) > 100:
        await message.answer("Пожалуйста, введите корректное имя (от 2 до 100 символов).")
        return
    await state.update_data(name=name)
    await show_q3(message, state)


# --- Q3: Is member ---

@router.callback_query(SurveyStates.q3_is_member, F.data.startswith("member:"))
async def on_q3(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(is_member=cb.data == "member:yes")
    await show_q4(cb, state)


@router.callback_query(SurveyStates.q3_is_member, F.data == "back")
async def on_q3_back(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await show_q2(cb, state)


# --- Q4: Sole owner ---

@router.callback_query(SurveyStates.q4_is_sole_owner, F.data.startswith("owner:"))
async def on_q4(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(is_sole_owner=cb.data == "owner:yes")
    await show_q5(cb, state)


@router.callback_query(SurveyStates.q4_is_sole_owner, F.data == "back")
async def on_q4_back(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await show_q3(cb, state)


# --- Q5: Debt period ---

@router.callback_query(SurveyStates.q5_debt_period, F.data.startswith("period:"))
async def on_q5(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(debt_period=PERIOD_LABELS[cb.data])
    await show_q6(cb, state)


@router.callback_query(SurveyStates.q5_debt_period, F.data == "back")
async def on_q5_back(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await show_q4(cb, state)


# --- Q6: Debt amount ---

@router.callback_query(SurveyStates.q6_debt_amount, F.data.startswith("amount:"))
async def on_q6(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(debt_amount=AMOUNT_LABELS[cb.data])
    await show_q7(cb, state)


@router.callback_query(SurveyStates.q6_debt_amount, F.data == "back")
async def on_q6_back(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await show_q5(cb, state)


# --- Q7: Actions taken (multi-select) ---

@router.callback_query(SurveyStates.q7_actions, F.data.startswith("act:"))
async def on_q7(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("actions_selected", [])

    if cb.data == "act:done":
        if not selected:
            await cb.answer("Выберите хотя бы один вариант.", show_alert=True)
            return
        await cb.answer()
        labels = [ACTION_LABELS[s] for s in selected]
        await state.update_data(actions_taken=labels)
        if "act:other" in selected:
            await state.set_state(SurveyStates.q7_actions_other)
            await cb.message.edit_text(
                "Вопрос 7 (доп.)\n\nОпишите, какие иные действия Вы предпринимали:"
            )
        else:
            await state.update_data(actions_other=None)
            await show_q8(cb, state)
        return

    await cb.answer()
    if cb.data in selected:
        selected.remove(cb.data)
    else:
        selected.append(cb.data)
    await state.update_data(actions_selected=selected)
    await cb.message.edit_reply_markup(reply_markup=kb_q7_actions(selected))


@router.callback_query(SurveyStates.q7_actions, F.data == "back")
async def on_q7_back(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(actions_selected=[])
    await show_q6(cb, state)


# --- Q7 other (text input) ---

@router.message(SurveyStates.q7_actions_other)
async def on_q7_other(message: Message, state: FSMContext):
    text = message.text.strip() if message.text else ""
    if len(text) < 2:
        await message.answer("Пожалуйста, опишите подробнее (минимум 2 символа).")
        return
    await state.update_data(actions_other=text)
    await show_q8(message, state)


# --- Q8: Written response ---

@router.callback_query(SurveyStates.q8_written_response, F.data.startswith("written:"))
async def on_q8(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(has_written_response=cb.data == "written:yes")
    await show_q9(cb, state)


@router.callback_query(SurveyStates.q8_written_response, F.data == "back")
async def on_q8_back(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    data = await state.get_data()
    selected = data.get("actions_selected", [])
    if "act:other" in selected:
        await state.set_state(SurveyStates.q7_actions_other)
        await cb.message.edit_text(
            "Вопрос 7 (доп.)\n\nОпишите, какие иные действия Вы предпринимали:"
        )
    else:
        await show_q7(cb, state)


# --- Q9: Debtor data (multi-select) ---

@router.callback_query(SurveyStates.q9_debtor_data, F.data.startswith("data:"))
async def on_q9(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    selected = data.get("debtor_data_selected", [])

    if cb.data == "data:done":
        if not selected:
            await cb.answer("Выберите хотя бы один вариант.", show_alert=True)
            return
        await cb.answer()
        labels = [DATA_LABELS[s] for s in selected]
        await state.update_data(debtor_data=labels)
        await show_q10(cb, state)
        return

    await cb.answer()
    if cb.data in selected:
        selected.remove(cb.data)
    else:
        selected.append(cb.data)
    await state.update_data(debtor_data_selected=selected)
    await cb.message.edit_reply_markup(reply_markup=kb_q9_debtor_data(selected))


@router.callback_query(SurveyStates.q9_debtor_data, F.data == "back")
async def on_q9_back(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.update_data(debtor_data_selected=[])
    await show_q8(cb, state)


# --- Q10: Phone ---

PHONE_RE = re.compile(r"^(\+7|8)\d{10}$")


@router.message(SurveyStates.q10_phone)
async def on_q10(message: Message, state: FSMContext):
    raw = message.text.strip() if message.text else ""
    phone = raw.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if not PHONE_RE.match(phone):
        await message.answer(
            "Неверный формат. Введите российский номер: +7XXXXXXXXXX или 8XXXXXXXXXX"
        )
        return
    await state.update_data(
        contact_phone=phone,
        telegram_id=message.from_user.id,
        telegram_username=message.from_user.username,
    )

    from db import save_survey
    from handlers.notify import send_notification

    data = await state.get_data()
    survey_id = await save_survey(data)
    await send_notification(message.bot, data, survey_id)

    await message.answer(
        "Спасибо за предоставленную информацию!\n"
        "В ближайшее время наши специалисты свяжутся с Вами.",
        reply_markup=kb_confirm_another(),
    )
    await state.set_state(SurveyStates.confirm_another)


# --- Confirm another survey ---

@router.callback_query(SurveyStates.confirm_another, F.data == "another:yes")
async def on_another_yes(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.clear()
    await show_q1(cb, state)


@router.callback_query(SurveyStates.confirm_another, F.data == "another:no")
async def on_another_no(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    await state.clear()
    await cb.message.edit_text("Спасибо! Если понадобится помощь — нажмите /start")
