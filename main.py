#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fazelFinder import fazelFinder

from config import TelegramToken

from telegram.ext import Updater, CommandHandler, Filters, MessageHandler

updater = Updater(token=TelegramToken, use_context=True)
dispatcher = updater.dispatcher
import logging
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
fazel_set = set()
new_fazel_set = set()
def notify(context):
    global fazel_set
    global new_fazel_set
    new_fazel = fazelFinder("https://www.doctolib.de/impfung-covid-19-corona/53115-bonn?ref_visit_motive_ids[]=6768&ref_visit_motive_ids[]=6936")
    new_fazel += fazelFinder("https://www.doctolib.de/impfung-covid-19-corona/50667-koeln?ref_visit_motive_ids[]=6768&ref_visit_motive_ids[]=6936")
    new_fazel += fazelFinder("https://www.doctolib.de/impfung-covid-19-corona/40210-duesseldorf?ref_visit_motive_ids[]=6768&ref_visit_motive_ids[]=6936")
    if new_fazel:
        for item in new_fazel:
            new_fazel_set.add(item[1])
        tmp_set = new_fazel_set.difference(fazel_set) if fazel_set else new_fazel_set
        for item in tmp_set:
            new_item = [fazel for fazel in new_fazel if fazel[1] == item]
            if new_item[0][0] == -1:
                text = "one appointment found for " + new_item[0][2] + ". Link:\n" + new_item[0][1]
            else:
                text = str(new_item[0][0]) + " appointment for this week found. Link:\n" + new_item[0][1]
            if "bottrop" not in new_item[0][1]:
                context.bot.send_message(chat_id="@BotUcontacti", text=text)
        fazel_set = new_fazel_set
    else:
        fazel_set = set()
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hellooo!!")

def timer(update, context):
    chat_id = update.message.chat_id
    new_job = context.job_queue.run_repeating(notify, interval = 60, context=chat_id)
    context.chat_data['job'] = new_job
    update.message.reply_text('Notifier successfully set!')

def unset(update, context):
    """Remove the job if the user changed their mind."""
    if 'job' not in context.chat_data:
        update.message.reply_text('You have no active notifier')
        return

    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']

    update.message.reply_text('Notifier successfully unset!')

def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


def main():

    daily = CommandHandler('fazel', timer, pass_job_queue=True, pass_chat_data=True)
    dispatcher.add_handler(daily)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    dispatcher.add_handler(CommandHandler('unset', unset, pass_chat_data=True))

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    updater.start_polling()
    # updater.idle()

    return 0

if __name__ == "__main__":
    main()
