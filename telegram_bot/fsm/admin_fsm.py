from aiogram.fsm.state import State, StatesGroup 

class UserListStates(StatesGroup):
    GetOffset = State()
    GetLimit = State()
    AddUserID = State()
    GetUserIDToRemove = State()
    GetUserIDForFetch = State()