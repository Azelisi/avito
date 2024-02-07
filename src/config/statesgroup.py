from aiogram.fsm.state import State, StatesGroup


class MainStateGroup(StatesGroup): 
    main = State()

class ParsingAvito(StatesGroup): 
    main = State() 

