# -*- coding: utf-8 -*-

# City Guide: A sample Alexa Skill Lambda function
# This function shows how you can manage data in objects and arrays,
# choose a random recommendation,
# call an external API and speak the result,
# handle YES/NO intents with session attributes,
# and return text data on a card.

import logging
import random
import gettext

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor)
from ask_sdk_core.utils import is_intent_name, is_request_type

from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

from alexa import data, util

# Skill Builder object
sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Request Handler classes
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        # logger.info(_("This is an untranslated message"))

        speech = _(data.WELCOME)
        speech += " " + _(data.HELP)
        handler_input.response_builder.speak(speech)
        handler_input.response_builder.ask(_(
            data.GENERIC_REPROMPT))
        return handler_input.response_builder.response


class AboutIntentHandler(AbstractRequestHandler):
    """Handler for about intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AboutIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In AboutIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(data.ABOUT))
        return handler_input.response_builder.response


class CoffeeIntentHandler(AbstractRequestHandler):
    """Handler for coffee intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("CoffeeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CoffeeIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes

        restaurant = random.choice(util.get_restaurants_by_meal(
            data.CITY_DATA, "coffee"))
        session_attr["restaurant"] = restaurant["name"]
        speech = ("For a great coffee shop, I recommend {}. Would you "
                  "like to hear more?").format(restaurant["name"])

        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class BreakfastIntentHandler(AbstractRequestHandler):
    """Handler for breakfast intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("BreakfastIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In BreakfastIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes

        restaurant = random.choice(util.get_restaurants_by_meal(
            data.CITY_DATA, "breakfast"))
        session_attr["restaurant"] = restaurant["name"]
        speech = ("For breakfast, try this. {}. Would you "
                  "like to hear more?").format(restaurant["name"])

        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class LunchIntentHandler(AbstractRequestHandler):
    """Handler for lunch intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LunchIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LunchIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes

        restaurant = random.choice(util.get_restaurants_by_meal(
            data.CITY_DATA, "lunch"))
        session_attr["restaurant"] = restaurant["name"]
        speech = ("Lunch time! Here is a good spot. {}. Would you "
                  "like to hear more?").format(restaurant["name"])

        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class DinnerIntentHandler(AbstractRequestHandler):
    """Handler for dinner intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("DinnerIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In DinnerIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes

        restaurant = random.choice(util.get_restaurants_by_meal(
            data.CITY_DATA, "dinner"))
        session_attr["restaurant"] = restaurant["name"]
        speech = ("Enjoy dinner at, {}. Would you "
                  "like to hear more?").format(restaurant["name"])

        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


class YesMoreInfoIntentHandler(AbstractRequestHandler):
    """Handler for yes to get more info intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.YesIntent")(handler_input) and
                "restaurant" in session_attr)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In YesMoreInfoIntentHandler")

        attribute_manager = handler_input.attributes_manager
        session_attr = attribute_manager.session_attributes
        _ = attribute_manager.request_attributes["_"]

        restaurant_name = session_attr["restaurant"]
        restaurant_details = util.get_restaurants_by_name(
            data.CITY_DATA, restaurant_name)

        speech = ("{} is located at {}, the phone number is {}, and the "
                  "description is, {}. I have sent these details to the "
                  "Alexa App on your phone.  Enjoy your meal! "
                  "<say-as interpret-as='interjection'>bon appetit</say-as>"
                  .format(restaurant_details["name"],
                          restaurant_details["address"],
                          restaurant_details["phone"],
                          restaurant_details["description"]))
        card_info = "{}\n{}\n{}, {}, {}\nphone: {}\n".format(
            restaurant_details["name"], restaurant_details["address"],
            data.CITY_DATA["city"], data.CITY_DATA["state"],
            data.CITY_DATA["postcode"], restaurant_details["phone"])

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(
                title=_(data.SKILL_NAME),
                content=card_info)).set_should_end_session(True)
        return handler_input.response_builder.response


class NoMoreInfoIntentHandler(AbstractRequestHandler):
    """Handler for no to get no more info intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.NoIntent")(handler_input) and
                "restaurant" in session_attr)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In NoMoreInfoIntentHandler")

        speech = ("Ok.  Enjoy your meal! "
                  "<say-as interpret-as='interjection'>bon appetit</say-as>")
        handler_input.response_builder.speak(speech).set_should_end_session(
            True)
        return handler_input.response_builder.response


class AttractionIntentHandler(AbstractRequestHandler):
    """Handler for attraction intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AttractionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In AttractionIntentHandler")
        distance = util.get_resolved_value(
            handler_input.request_envelope.request, "distance")
        if distance is None:
            distance = 200

        attraction = random.choice(util.get_attractions_by_distance(
            data.CITY_DATA, distance))
        speech = "Try {}, which is {}. {}. Have fun!!".format(
            attraction["name"],
            "right downtown" if attraction["distance"] == "0"
            else "{} miles away".format(attraction["distance"]),
            attraction["description"])

        handler_input.response_builder.speak(speech).set_should_end_session(
            True)
        return handler_input.response_builder.response


class GoOutIntentHandler(AbstractRequestHandler):
    """Handler for go out intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("GoOutIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GoOutIntentHandler")
        local_time, current_temp, current_condition = util.get_weather(
            data.CITY_DATA, data.MY_API)

        speech = "It is {} and the weather in {} is {} and {}.".format(
            local_time, data.CITY_DATA["city"], current_temp,
            current_condition)

        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for skill session end."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for help intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.HELP)).ask(_(data.HELP))
        return handler_input.response_builder.response


class ExitIntentHandler(AbstractRequestHandler):
    """Single Handler for Cancel, Stop intents."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.STOP)).set_should_end_session(True)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for handling fallback intent or Yes/No without
    restaurant info intent.

     2018-May-01: AMAZON.FallackIntent is only currently available in
     en-US locale. This handler will not be triggered except in that
     locale, so it can be safely deployed for any locale."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        session_attr = handler_input.attributes_manager.session_attributes
        return (is_intent_name("AMAZON.FallbackIntent")(handler_input) or
                ("restaurant" not in session_attr and (
                    is_intent_name("AMAZON.YesIntent")(handler_input) or
                    is_intent_name("AMAZON.NoIntent")(handler_input))
                 ))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        _ = handler_input.attributes_manager.request_attributes["_"]

        handler_input.response_builder.speak(_(
            data.FALLBACK).format(data.SKILL_NAME)).ask(_(
            data.FALLBACK).format(data.SKILL_NAME))

        return handler_input.response_builder.response


# Exception Handler classes
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch All Exception handler.

    This handler catches all kinds of exceptions and prints
    the stack trace on AWS Cloudwatch with the request envelope."""
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        logger.info("Original request was {}".format(
            handler_input.request_envelope.request))

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


class LocalizationInterceptor(AbstractRequestInterceptor):
    """Add function to request attributes, that can load locale specific data."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        locale = handler_input.request_envelope.request.locale
        logger.info("Locale is {}".format(locale))
        i18n = gettext.translation(
            'base', localedir='locales', languages=[locale], fallback=True)
        handler_input.attributes_manager.request_attributes[
            "_"] = i18n.gettext


# Add all request handlers to the skill.
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AboutIntentHandler())
sb.add_request_handler(CoffeeIntentHandler())
sb.add_request_handler(BreakfastIntentHandler())
sb.add_request_handler(LunchIntentHandler())
sb.add_request_handler(DinnerIntentHandler())
sb.add_request_handler(YesMoreInfoIntentHandler())
sb.add_request_handler(NoMoreInfoIntentHandler())
sb.add_request_handler(AttractionIntentHandler())
sb.add_request_handler(GoOutIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Add locale interceptor to the skill.
sb.add_global_request_interceptor(LocalizationInterceptor())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()
