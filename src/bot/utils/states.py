from aiogram.fsm.state import State, StatesGroup


class StatesMachine(StatesGroup):
    get_admin_username = State()
    get_user_id_to_remove = State()
