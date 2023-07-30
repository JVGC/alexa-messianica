from datetime import date

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response


from app.spreadsheet import get_sacred_word_by_date


class TodaysSacredWordIntentHandler(AbstractRequestHandler):
    """Handler for Today's Sacred Word Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TodaysSacredWordIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        sacred_word = get_sacred_word_by_date(date.today().strftime(format="%d/%m/%Y"))

        return (
            handler_input.response_builder.speak(
                f"Leitura do Ensinamento: {sacred_word.title}. {sacred_word.content}"
            )
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )