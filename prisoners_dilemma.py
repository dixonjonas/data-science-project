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

    #Function to extract 'Cooperate' or 'Betray' from Agent response
    def extract_responses(self, initial_responses):
        extracted_responses = []
        for index, response in enumerate(initial_responses):
            if "Cooperate" in response:
                extracted_responses.append("Agent " + str(index+1) + " chooses to cooperate")
            elif "Betray" in response:
                extracted_responses.append("Agent " + str(index+1) + " chooses to betray")
        
        return extracted_responses

    #TODO add prison sentence function

    #Function to run prisoners dilemma with no history
    def run_single_round(self):
        #Creating agents
        agent1 = Agent(self.rewards)
        agent2 = Agent(self.rewards)

        #Getting the agent responses
        agent1_response = agent1.call('')['message']['content']
        agent2_response = agent1.call('')['message']['content']
        initial_responses = [agent1_response, agent2_response]

        #Extracting responses
        responses = self.extract_responses(initial_responses)

        #TODO add the final prison sentence to the output

        return responses

    #Function to run iterated prisoners dilemma with history
    def run_multi_round(self, number_of_rounds):
        #TODO add multi-round prisoners dilemma with history
        return None