from aiogram.fsm.state import State, StatesGroup


class SurveyStates(StatesGroup):
    q1_role = State()
    q2_name = State()
    q3_is_member = State()
    q4_is_sole_owner = State()
    q5_debt_period = State()
    q6_debt_amount = State()
    q7_actions = State()
    q7_actions_other = State()
    q8_written_response = State()
    q9_debtor_data = State()
    q10_phone = State()
    confirm_another = State()
