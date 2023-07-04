""" Lambda Funtion """
import logging

from ask_sdk_core.skill_builder import SkillBuilder

from app.intents.default import (
    CancelOrStopIntentHandler,
    HelpIntentHandler,
    FallbackIntentHandler,
    SessionEndedRequestHandler,
    IntentReflectorHandler,
    CatchAllExceptionHandler,
)
from app.intents.launch import LaunchRequestHandler
from app.intents.experience import TodaysExperienceIntentHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(TodaysExperienceIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(
    IntentReflectorHandler()
)  # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
