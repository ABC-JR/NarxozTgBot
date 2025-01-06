class SendGroup:

    # Два варианта для опроса
    option = ["Поддерживаю", "Не поддерживаю"]

    @staticmethod
    async def sendtochat(bot, channid, category, question):
        poll_question = f"📢 Петиция по теме '{category}':\n\n{question}"
        await bot.send_poll(chat_id=channid, question=poll_question, options=SendGroup.option, is_anonymous=True)