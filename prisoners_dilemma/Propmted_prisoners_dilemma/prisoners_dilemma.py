import ollama
import sys
import csv
import random
from agent import Agent

class prisonersDilemma:
    def __init__(self, rewards) -> None:
        self.agents = []
        self.history_p1 = ""
        self.history_p2 = ""
        self.rewards = rewards
        self.game_prompt = """You are participating in a game called the "Prisoner's Dilemma." In this game, you and another prisoner are being questioned separately. Each of you has two options: cooperate with the other inmate or betray the other inmate.
                                    If both inmates cooperate, you each will serve """ + self.rewards[0] + """ years in prison.
                                    If both inmates betray, you each will serve """ + self.rewards[1] + """ years in prison.
                                    If one inmate betrays while the other cooperates, the betrayer will serve """ + self.rewards[3] + """ years in prison, while the cooperator will serve """ + self.rewards[2] + """" years in prison.
                                    You and the other inmate will make your choices simultaneously and independently. Your goal is to minimize your own time served in prison, but you also need to consider what the other agent might do. 
                                    Make your decision: cooperate or betray? Always respond with only "Cooperate" or "Betray", do not write anything else. """
        self.agent1 = Agent(self.game_prompt)
        self.agent2 = Agent(self.game_prompt)
        self.big_five_p1 = {}
        self.big_five_p2 = {}

    #Set the mode of the prisoners dilemma
    def get_mode():
        try:
            print("")
            mode = input("Please enter 'Standard' for the standard prisoners dilemma or 'Iterated' for the iterated prisoners dilemma: ")
            print("")
            if mode.lower() == "standard" or mode.lower() == "iterated":
                return mode.lower()
            else:
                raise ValueError(f"Invalid input: {mode}. Please enter 'Standard' or 'Iterated'.")
        except ValueError as e:
            print(e)
            sys.exit(1)
    
    #Get the number of rounds from the user
    def get_rounds(self):
        round_integer = 0
        try:
            rounds = input("Please enter the number of rounds you want to run the simulation for (up to 10000): ")
            print("")
            round_integer = int(rounds)
            if round_integer > 10000:
                raise ValueError("Invalid input! Please enter an integer no larger than 10000.")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")
            sys.exit(1)
     
        return round_integer

    #Function to call the LLM agents to generate a response
    def call_agents(self, history_agent1, history_agent2):
        big_five_dict_p1 = {
            'Openness': "",
            'Conscientiousness': "",
            'Extraversion': "",
            'Agreeableness': "",
            'Neuroticism': ""
        }

        big_five_dict_p2 = {
            'Openness': "",
            'Conscientiousness': "",
            'Extraversion': "",
            'Agreeableness': "",
            'Neuroticism': ""
        }

        for category in big_five_dict_p1:
            if self.big_five_p1[category] != 'random':
                big_five_dict_p1[category] = self.big_five_p1[category]
            else:
                big_five_dict_p1[category] = Agent.assign_trait()

        for category in big_five_dict_p2:
            if self.big_five_p2[category] != 'random':
                big_five_dict_p2[category] = self.big_five_p2[category]
            else:
                 big_five_dict_p2[category] = Agent.assign_trait()
        print(big_five_dict_p1)

        agent1_response = ""
        agent2_response = ""
        while True:
            agent1_response = self.agent1.call(history_agent1, big_five_dict_p1)['message']['content']
            if "cooperate" in agent1_response.lower() or "betray" in agent1_response.lower():
                break
        while True:
            agent2_response = self.agent2.call(history_agent2, big_five_dict_p2)['message']['content']
            if "cooperate" in agent2_response.lower() or "betray" in agent2_response.lower():
                break

        return agent1_response, agent2_response

    #Function to extract 'Cooperate' or 'Betray' from Agent response
    def extract_responses(self, initial_responses):
        extracted_responses = []
        for index, response in enumerate(initial_responses):
            if "cooperate" in response.lower():
                extracted_responses.append("Prisoner " + str(index+1) + " chooses to cooperate")
            elif "betray" in response.lower():
                extracted_responses.append("Prisoner " + str(index+1) + " chooses to betray")
        
        return extracted_responses

    #Find the sentence for the prisoners 
    def calculate_sentence_and_results(self, extracted_responses, rewards):
        result_cooperation = [0,0]
        sentence = ""
        if "cooperate" in extracted_responses[0].lower() and "cooperate" in extracted_responses[1].lower():
            sentence = "Both prisoners are sentenced to " + rewards[0] + " year(s) in prison"
            result_cooperation[0] = 1
            result_cooperation[1] = 1
        elif "betray" in extracted_responses[0].lower() and "betray" in extracted_responses[1].lower():
            sentence = "Both prisoners are sentenced to " + rewards[1] + " year(s) in prison"
        elif "betray" in extracted_responses[0].lower() and "cooperate" in extracted_responses[1].lower():
            sentence = "Prisoner 1 is sentenced to " + rewards[3] + " and prisoner 2 is sentenced to " + rewards[2] + " year(s) in prison"
            result_cooperation[1] = 1
        elif "cooperate" in extracted_responses[0].lower() and "betray" in extracted_responses[1].lower():
            sentence = "Prisoner 1 is sentenced to " + rewards[2] + " and prisoner 2 is sentenced to " + rewards[3] + " year(s) in prison"
            result_cooperation[0] = 1

        return sentence, result_cooperation

    #Function to run the prisoners dilemma
    def run_prisoners_dilemma(self, mode) -> None:
        #Creating .csv file
        with open('prisoners_dilemma_results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Game', 'Prisoner 1 Response', 'Prisoner 2 Response', 'Sentence'])       

            #Asking user for how many rounds they want to run
            rounds = self.get_rounds()

            #Asking the user for personality inputs
            self.big_five_p1 = self.agent1.get_big_five("prisoner 1")
            self.big_five_p2 = self.agent2.get_big_five("prisoner 2")

            #Running simulation for specified number of rounds
            results = [0,0]
            for i in range(rounds):
                #Generating the agent responses
                if mode == 'iterated':
                    agent1_response, agent2_response = self.call_agents(self.history_p1, self.history_p2)
                elif mode == 'standard':
                    agent1_response, agent2_response = self.call_agents('', '')
                initial_responses = [agent1_response, agent2_response]

                #Extracting responses
                responses = self.extract_responses(initial_responses)

                #Calculating sentence
                sentence, result_cooperation = self.calculate_sentence_and_results(responses, self.rewards)

                #Write round result to CSV
                writer.writerow([i+1, initial_responses[0], initial_responses[1], sentence])

                #Aggregating results
                results[0] = results[0] + result_cooperation[0]
                results[1] = results[1] + result_cooperation[1]

                #Adding to the history
                if i == 0:
                    self.history_p1 = self.history_p1 + "This is the history of previous rounds. Consider it when making a decision."
                    self.history_p2 = self.history_p2 + "This is the history of previous rounds. Consider it when making a decision."
                i_plus = i+1
                if results[1] == 1:
                    self.history_p1 = self.history_p1 + f"\nRound {i_plus}: The other prisoner cooperated!"
                elif results[1] == 0:
                    self.history_p1 = self.history_p1 + f"\nRound {i_plus}: The other prisoner betrayed!"
                if results[0] == 1:
                    self.history_p2 = self.history_p2 + f"\nRound {i_plus}: The other prisoner cooperated!"
                elif results[0] == 0:
                    self.history_p2 = self.history_p2 + f"\nRound {i_plus}: The other prisoner betrayed!"

                #Printing responses and sentence
                print(f"Game {i_plus}: " )
                print(f"    {responses[0]}")
                print(f"    {responses[1]}")
                print("")
                print(f"    {sentence}")
                print("")
        
            #Printing final result
            print("Prisoner 1 cooperated " + str(results[0]) + " times and betrayed " + str(rounds-results[0]) + " times")
            print("Prisoner 2 cooperated " + str(results[1]) + " times and betrayed " + str(rounds-results[1]) + " times")
            print("")
            
            
