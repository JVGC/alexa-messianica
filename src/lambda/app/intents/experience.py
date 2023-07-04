import ask_sdk_core.utils as ask_utils

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from datetime import date

from app.spreadsheet.experience_repository import ExperienceSheetRepository


class TodaysExperienceIntentHandler(AbstractRequestHandler):
    """Handler for Today's Sacred Word Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TodaysExperienceIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        experience_repository = ExperienceSheetRepository()
        experience = experience_repository.getByDate(
            date.today().strftime(format="%d/%m/%Y")
        )

        return (
            handler_input.response_builder.speak(
                f"Experiência de fé de {experience.person_name}. {experience.church}. {experience.content}"
            )
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )
