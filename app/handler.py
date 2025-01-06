# from gc import callbacks
# from pickletools import markobject
#
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.types import Message, CallbackQuery
# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from unicodedata import category
#
# from sendingtogroups import SendGroup
# from aiogram.filters import Command
# from aiogram import Bot, Dispatcher, types
# from aiogram import Router
#
# API_TOKEN = "8198728804:AAFpmPJ820ZVGVgc5LBS_IHnbjkcpPoV6oo"
# CHANNEL_ID = "-4583360988"
#
#
#
# bot = Bot(token=API_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(storage=storage)
#
#
# router = Router()
#
# # Start command handler
# @router.message(Command("start"))
# async def start(message: Message):
#     await message.answer("Привет! Ты здесь можешь сделать петицию или пожаловаться ректору анонимно.")
#     markup = InlineKeyboardBuilder()
#     markup.button(text="Создавать новую петицию", callback_data='petition')
#     markup.button(text="Жалобы на ректора", callback_data='zhalob')
#     await message.answer("Выберите действие:", reply_markup=markup.as_markup())
#
#
# # Petition callback handler
# @router.callback_query(lambda call: call.data == "petition")
# async def handle_petition(call: CallbackQuery):
#
#
#     markup = InlineKeyboardBuilder()
#     markup.button(text= 'инфраструктура' , callback_data ="infastur")
#     markup.button(text='образование' , callback_data='education')
#     markup.button(text='Социальные мероприятия', callback_data="Social")
#     markup.button(text='Экологические вопросы' , callback_data='Environmental')
#     markup.button(text='Вопросы безопасности' , callback_data='Security')
#     markup.button(text='Others' , callback_data='others')
#     await call.message.answer("выберите категорию", reply_markup=markup.as_markup())
#
#
#
#
#
#
#     # Set up a message handler to capture the petition question
#
#
# @router.callback_query(lambda call: call.data == "infastur" or
#                                   call.data == "education" or
#                                   call.data == "Social" or
#                                   call.data == "Security" or
#                                   call.data == "others" or
#                                   call.data == "Environmental")
#
# async def handlebuttons(call : CallbackQuery):
#     category = ""
#
#     if call.data== "infastur":
#         category = "инфраструктура"
#
#         await call.message.edit_text("инфраструктура")
#     if call.data== "education":
#         category = "образование"
#         await call.message.edit_text("образование")
#     if call.data== "Social":
#         category = "Социальные мероприятия"
#         await call.message.edit_text("Социальные мероприятия")
#     if call.data== "Environmental":
#         category = "Экологические вопросы"
#         await call.message.edit_text("Экологические вопросы")
#     if call.data== "Security":
#         category = "Вопросы безопасности"
#         await call.message.edit_text("Вопросы безопасности")
#     if call.data== "others":
#
#         call.message.edit_text("Укажите категорию вашего петицию")
#         @router.message(lambda message:True)
#         async def categorymannual(message: types.Message):
#             category = message.text
#             await call.message.edit(category)
#
#
#     await call.message.answer("Ваш петеция ? ")
#     @router.message(lambda message: True)
#     async def capture_question(message: types.Message):
#
#         question = message.text
#         await SendGroup.sendtochat(bot, CHANNEL_ID,category ,  question)
#         await message.answer("Петиция отправлена в канал!")
#
#
# # Rector complaint callback handler
# @router.callback_query(lambda call: call.data == "zhalob")
# async def handle_zhalob(call: CallbackQuery):
#     await call.message.answer("Отправьте вашу жалобу в виде сообщения.")
#

from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, CallbackQuery
from aiogram import Router
from sendingtogroups import SendGroup

API_TOKEN = "8198728804:AAFpmPJ820ZVGVgc5LBS_IHnbjkcpPoV6oo"
CHANNEL_ID = "-4583360988"

# Создание экземпляра Bot
bot = Bot(token=API_TOKEN)

# Создание объекта Router
router = Router()

# Определение состояний
class Form(StatesGroup):
    waiting_for_category = State()
    waiting_for_petition_text = State()

# Обработчик команды /start
@router.message(Command("start"))
async def start(message: Message):
    welcome_text = (
        "👋 Привет! Добро пожаловать в бота для создания петиций и жалоб!\n\n"
        "Здесь ты можешь:\n"
        "📄 Создать новую петицию\n"
        "📝 Анонимно пожаловаться ректору"
    )
    markup = InlineKeyboardBuilder()
    markup.button(text="📄 Создать петицию", callback_data='petition')
    markup.button(text="📝 Жалоба на ректора", callback_data='zhalob')
    await message.answer(welcome_text, reply_markup=markup.as_markup())

# Обработчик для создания петиции
@router.callback_query(lambda call: call.data == "petition")
async def handle_petition(call: CallbackQuery, state: FSMContext):
    markup = InlineKeyboardBuilder()
    markup.button(text="🏢 Инфраструктура", callback_data="infrastructure")
    markup.button(text="📚 Образование", callback_data="education")
    markup.button(text="🛡️ Безопасность", callback_data="security")
    markup.button(text="♻️ Экология", callback_data="environment")
    markup.button(text="🎉 Соц. мероприятия", callback_data="social")
    markup.button(text="❓ Другое", callback_data="other")
    await call.message.edit_text("🔍 Пожалуйста, выберите категорию для вашей петиции:", reply_markup=markup.as_markup())
    await state.set_state(Form.waiting_for_category)  # Исправлено

# Обработчик выбора категории
@router.callback_query(lambda call: call.data in ["infrastructure", "education", "security", "environment", "social", "other"])
async def handle_category(call: CallbackQuery, state: FSMContext):
    category = call.data
    await state.update_data(category=category)

    if category == "other":
        await call.message.edit_text("📝 Укажите категорию вашего петиции вручную:")
        await state.set_state(Form.waiting_for_petition_text)  # Исправлено
    else:
        await call.message.edit_text(f"✅ Категория выбрана: {category}\n\n✏️ Введите текст петиции:")
        await state.set_state(Form.waiting_for_petition_text)  # Исправлено

# Обработчик для ввода текста петиции
@router.message(StateFilter(Form.waiting_for_petition_text))
async def capture_petition(message: Message, state: FSMContext):
    data = await state.get_data()
    category = data.get("category")
    petition_text = message.text
    await SendGroup.sendtochat(bot, CHANNEL_ID, category, petition_text)
    await message.answer("✅ Ваша петиция отправлена на рассмотрение!")
    await state.finish()  # Завершить состояние

# Обработчик жалобы на ректора
@router.callback_query(lambda call: call.data == "zhalob")
async def handle_zhalob(call: CallbackQuery):
    await call.message.answer("📝 Пожалуйста, отправьте вашу жалобу в виде текста:")

# Обработчик для текста жалобы
@router.message(StateFilter("*"))  # Обработчик для любого состояния
async def capture_complaint(message: Message, state: FSMContext):
    complaint_text = message.text
    await SendGroup.sendtochat(bot, CHANNEL_ID, "Жалоба", complaint_text)  # Передача текста жалобы
    await message.answer("✅ Ваша жалоба отправлена на рассмотрение!")