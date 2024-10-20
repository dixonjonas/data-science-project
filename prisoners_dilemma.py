import ollama
import json
import os
import time
from agent import Agent

class prisonersDilemma:
    def __init__(self, rewards) -> None:
        self.agents = []
        self.history = []
        self.rewards = rewards
        self.game_prompt = """You are participating in a game called the "Prisoner's Dilemma." In this game, you and another prisoner are being questioned separately. Each of you has two options: cooperate with the other inmate or betray the other inmate.
                                    If both inmates cooperate, you each will serve """ + self.rewards[0] + """ years in prison.
                                    If both inmates betray, you each will serve """ + self.rewards[1] + """ years in prison.
                                    If one inmate betrays while the other cooperates, the betrayer will serve """ + self.rewards[3] + """ years in prison, while the cooperator will serve """ + self.rewards[2] + """" years in prison.
                                    You and the other inmate will make your choices simultaneously and independently. Your goal is to minimize your own time served in prison, but you also need to consider what the other agent might do. 
                                    Make your decision: cooperate or betray? Please only respond with either "Cooperate" or "Betray" """

    #Set the mode of the prisoners dilemma
    def get_mode():
        try:
            print("")
            mode = input("Please enter 'single' for normal prisoners dilemma or 'multi' for iterated prisoners dilemma: ")
            print("")
            if mode.lower() == "single" or mode.lower() == "multi":
                return mode.lower()
            else:
                raise ValueError(f"Invalid input: {mode}. Please enter 'single' or 'multi'.")
        except ValueError as e:
            print(e)

    #Function to extract 'Cooperate' or 'Betray' from Agent response
    def extract_responses(self, initial_responses):
        extracted_responses = []
        for index, response in enumerate(initial_responses):
            if "Cooperate" in response:
                extracted_responses.append("Prisoner " + str(index+1) + " chooses to cooperate")
            elif "Betray" in response:
                extracted_responses.append("Prisoner " + str(index+1) + " chooses to betray")
        
        return extracted_responses

    #Find the sentence for the prisoners 
    def calculate_sentence(self, extracted_responses, rewards):
        sentence = ""
        if "cooperate" in extracted_responses[0] and "cooperate" in extracted_responses[1]:
            sentence = "Both prisoners are sentenced to " + rewards[0] + " year(s) in prison"
        elif "betray" in extracted_responses[0] and "betray" in extracted_responses[1]:
            sentence = "Both prisoners are sentenced to " + rewards[1] + " year(s) in prison"
        elif "betray" in extracted_responses[0] and "cooperate" in extracted_responses[1]:
            sentence = "Prisoner 1 is sentenced to " + rewards[3] + " and prisoner 2 is sentenced to " + rewards[2] + " year(s) in prison"
        elif "cooperate" in extracted_responses[0] and "betray" in extracted_responses[1]:
            sentence = "Prisoner 1 is sentenced to " + rewards[2] + " and prisoner 2 is sentenced to " + rewards[3] + " year(s) in prison"

        return sentence

    #Function to run prisoners dilemma with no history
    def run_single_round(self):
        #Creating agents
        agent1 = Agent(self.game_prompt)
        agent2 = Agent(self.game_prompt)

        #Asking the user for personality inputs
        agent1.get_big_five("prisoner 1")
        agent2.get_big_five("prisoner 2")

        #Getting the agent responses
        agent1_response = agent1.call('')['message']['content']
        agent2_response = agent1.call('')['message']['content']
        initial_responses = [agent1_response, agent2_response]

        #Extracting responses
        responses = self.extract_responses(initial_responses)

        #Calculating sentence
        sentence = self.calculate_sentence(responses, self.rewards)

        return responses, sentence

    #Function to run iterated prisoners dilemma with history
    def run_multi_round(self, number_of_rounds):
        #TODO add multi-round prisoners dilemma with history
        return None