# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
import random

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType

# computer_choice & determine_winner functions refactored from
# https://github.com/thedanelias/rock-paper-scissors-python/blob/master/rockpaperscissors.py, MIT liscence
import requests
import ast
session = requests.Session()
session.auth = ("admin", "123456")

class ActionPlayRPS(Action):

    def name(self) -> Text:
        return "action_play_rps"

    def computer_choice(self):
        generatednum = random.randint(1, 3)
        if generatednum == 1:
            computerchoice = "rock"
        elif generatednum == 2:
            computerchoice = "paper"
        elif generatednum == 3:
            computerchoice = "scissors"

        return (computerchoice)

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # play rock paper scissors
        user_choice = tracker.get_slot("choice")
        dispatcher.utter_message(text=f"You chose {user_choice}")
        comp_choice = self.computer_choice()
        dispatcher.utter_message(text=f"The computer chose {comp_choice}")

        if user_choice == "rock" and comp_choice == "scissors":
            dispatcher.utter_message(text="Congrats, you won!")
        elif user_choice == "rock" and comp_choice == "paper":
            dispatcher.utter_message(text="The computer won this round.")
        elif user_choice == "paper" and comp_choice == "rock":
            dispatcher.utter_message(text="Congrats, you won!")
        elif user_choice == "paper" and comp_choice == "scissors":
            dispatcher.utter_message(text="The computer won this round.")
        elif user_choice == "scissors" and comp_choice == "paper":
            dispatcher.utter_message(text="Congrats, you won!")
        elif user_choice == "scissors" and comp_choice == "rock":
            dispatcher.utter_message(text="The computer won this round.")
        else:
            dispatcher.utter_message(text="It was a tie!")

        return []


class AnswerTheQuestion(Action):
    print("hi")

    def name(self) -> Text:
        return "answer_the_question"

    def get_the_ans(self, question):
        response = session.get('http://127.0.0.1:8000/api/get_answer/{}'.format(question))
        if isinstance(response.text, str):
            return response.text
        return ast.literal_eval(response.text)[0]['answer']

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # question = tracker.get_slot("question")
        current_state = tracker.current_state()
        question = current_state["latest_message"]["text"]
        print(question)

        ans = self.get_the_ans(question)
        dispatcher.utter_message(text=ans)

        return []


class ResponseForSelection(Action):

    def name(self) -> Text:
        return "response_for_selection"

    def get_the_recommendations(self):
        response = session.get("http://127.0.0.1:8000/api/machine_rec/")
        msg_dict = response.json()
        msg = "Top 3 Recommendations \n"
        for course,course_details in msg_dict.items():
            course_name = course_details[0]
            course_url = course_details[1]
            course_level = course_details[2]
            course_msg = "**Course {}** \n **Title:** {} \n Please click on **[Link]({})** \n **Level of Complexity:** {} \n".format(int(list(msg_dict).index(course))+1,course_name,course_url,course_level)
            msg = msg + course_msg
        return msg

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_choice = tracker.get_slot("options")
        if user_choice == "Finanical QA":
            dispatcher.utter_message(text="Please enter your question")
            dispatcher.utter_message()
        elif user_choice == "Recomendations":
            dispatcher.utter_message(
                text=self.get_the_recommendations())
            # dispatcher.utter_message(
            #     text="**Title:** Block chain with AI \n Please click on **[Link](https://www.udemy.com/python-for-finance-investment-fundamentals-data-analytics/)** \n **Number of ubscribers:** 1345")
        elif user_choice == "Infra Requests":
            # dispatcher.utter_message(text="Below are services we offer for Infra Request 1: 'Raise a Incident', 2:'Inquiry Incident'")
            dispatcher.utter_message(response="utter_infrarequest")
        return []


class ValidateRestaurantForm(Action):
    def name(self) -> Text:
        return "raise_incident_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["shortdescription", "description"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def create_incident(self,description,short_description):
        json_paylod = {"short_description": short_description, "description": description}
        response = session.post("http://127.0.0.1:8000/api/create_ticket/",json=json_paylod)
        response = response.json()
        incident_number = response['result']['number']
        return incident_number

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        short_description = tracker.get_slot("shortdescription")
        description = tracker.get_slot("description")
        res = self.create_incident(description,short_description)
        dispatcher.utter_message("Created Indcident and ID is:"+res)

class GetIncidentStatus(Action):
    def name(self) -> Text:
        return "response_incident_status"

    def get_incident_status(self,incidenid):
        response = session.get("http://127.0.0.1:8000/api/create_ticket/"+incidenid)
        response = response.json()
        incident_status = response[str(incidenid)]
        return incident_status

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        incidentid = tracker.get_slot("incidentid")
        res = self.get_incident_status(incidentid)
        if res == "No Record Found":
            msg = "No record found with incident id {} Please provide a valid ID".format(incidentid)
        else:
            msg = "Current status of incident {} is {}".format(incidentid, res)
        dispatcher.utter_message(msg)




