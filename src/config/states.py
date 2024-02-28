from aiogram.fsm.state import StatesGroup, State

# Машина состояний для отслеживания прогресса заполнения анкеты
class ParserStates(StatesGroup): 
    main_menu = State()
    parsing = State()