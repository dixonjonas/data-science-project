import ollama
import sys
import csv
import random
from agent import Agent

class ultimatumGame:
    def __init__(self) -> None:
        self.agents = []
        self.history_proposer = ""
        self.history_responder = ""
        self.proposer_prompt = """You are the Proposer in the Ultimatum Game. You are tasked with deciding how to split $100 between yourself and the Responder. 
                                    Your main goal is to maximize the amount of dollars($) you receive, but consider that if the Responder does reject your offer, none of you will get any money.
                                    The Responder is influenced by fairness and is likely to refuse an offer that it perceives as unfair.
                                    You can offer the Responder any amount of money between $0 and $100, as long as it is a whole number.
                                    Think strategically, balance fairness with your self-interest and make an offer that is likely to be accepted by the Responder.
                                    Your output should be a single whole number representing how much you will offer the Responder out of the $100. Do not write anything else. """

        self.responder_prompt = """You are the Responder in the Ultimatum Game. The Proposer has offered you a portion of $100 and you are tasked with deciding to 'accept' or 'reject' their offer.
                                    If you 'accept' the offer, you will split the money with the Proposer as offered.
                                    If you 'reject' the offer, you will both receive no money.
                                    You are influenced by fairness. You may reject offers that feel unfair, even if it means you receiving nothing.
                                    You should base your decision on a balance of fairness and practicality. If you reject an unfair offer it might teach the Proposer a lesson, but it could also lead to you receiving less money.
                                    Your output should be either: 'accept' if you accept the offer. Or 'reject' if you decide the offer is unfair and are willing to get nothing. Here is the proposal: """
                        
        self.proposer = Agent(self.proposer_prompt)
        self.responder = Agent(self.responder_prompt)
        self.big_five_proposer = {
            'Openness': "",
            'Conscientiousness': "",
            'Extraversion': "",
            'Agreeableness': "",
            'Neuroticism': ""
            }
        self.big_five_responder = {
            'Openness': "",
            'Conscientiousness': "",
            'Extraversion': "",
            'Agreeableness': "",
            'Neuroticism': ""
            }

    #Set the mode of the ultimatum game
    def get_mode():
        try:
            print("")
            mode = input("Please enter 'Standard' for the standard (one-shot) ultimatum game or 'Iterated' for the iterated ultimatum game: ")
            print("")
            if mode.lower() == "standard" or mode.lower() == "iterated":
                return mode.lower()
            else:
                raise ValueError(f"Invalid input: {mode}. Please enter 'Standard' or 'Iterated'.")
        except ValueError as e:
            print(e)
            sys.exit(1)

    #Get the number of games from the user
    def get_games(self):
        game_integer = 0
        try:
            games = input("Please enter the number of games you want to run the simulation for: ")
            print("")
            game_integer = int(games)
            if game_integer > 10000:
                raise ValueError("Invalid input! Please enter an integer no larger than 10000.")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")
            sys.exit(1)
        
        return game_integer
    
    #Get the number of rounds from the user
    def get_rounds(self):
        round_integer = 0
        try:
            rounds = input("Please enter the number of rounds you want to run the simulation for: ")
            print("")
            round_integer = int(rounds)
            if round_integer > 10000:
                raise ValueError("Invalid input! Please enter an integer no larger than 10000.")
        except ValueError:
            print("Invalid input! Please enter a valid integer.")
            sys.exit(1)
        
        return round_integer

    #Function to call the LLM agents to generate a response
    def call_agents(self, history_proposer, history_responder):
        big_five_dict_proposer = {
            'Openness': "",
            'Conscientiousness': "",
            'Extraversion': "",
            'Agreeableness': "",
            'Neuroticism': ""
        }

        big_five_dict_responder = {
            'Openness': "",
            'Conscientiousness': "",
            'Extraversion': "",
            'Agreeableness': "",
            'Neuroticism': ""
        }

        for category in big_five_dict_proposer:
            if self.big_five_proposer[category] != 'random':
                big_five_dict_proposer[category] = self.big_five_proposer[category]
            else:
                big_five_dict_proposer[category] = Agent.assign_trait()

        for category in big_five_dict_responder:
            if self.big_five_responder[category] != 'random':
                big_five_dict_responder[category] = self.big_five_responder[category]
            else:
                big_five_dict_responder[category] = Agent.assign_trait()

        proposer_proposal = ""
        responder_response = ""
        while True:
            proposer_proposal = self.proposer.call(history_proposer, big_five_dict_proposer, '')['message']['content']
            if int(proposer_proposal) >= 0 or int(proposer_proposal) <= 100:
                break
        while True:
            proposal_message = f"The proposer offers to give you {proposer_proposal} out of the total $100 pot"
            responder_response = self.responder.call(history_responder, big_five_dict_responder, proposal_message)['message']['content']
            if "accept" in responder_response.lower() or "reject" in responder_response.lower():
                break

        return proposer_proposal, responder_response

    #Function to extract 'accept' or 'reject' from Agent response
    def extract_proposal_response(self, initial_proposal_response):
        extracted = []
        extracted.append(initial_proposal_response[0])
        extracted.append("The Proposer offers $" + initial_proposal_response[0] + " to the Responder")
        if "accept" in initial_proposal_response[1].lower():
            extracted.append("The Responder accepts the Proposers offer")
        elif "reject" in initial_proposal_response[1].lower():
            extracted.append("The Responder rejects the Proposers offer")
        
        return extracted

    #Find the result of the offering
    def calculate_results(self, extracted):
        result_acceptance = 0
        offer_made = 0
        result = ""
        if "accept" in extracted[2].lower():
            result = "The Proposer receives $" + str(100 - int(extracted[0])) + " and the Responder receives $" + str(extracted[0])
            result_acceptance = 1
            offer_made = int(extracted[0])
        elif "reject" in extracted[2].lower():
            result = "Both the Proposer and Responder receive $0"
            offer_made = int(extracted[0])

        return result, result_acceptance, offer_made

    #Function to run the ultimatum game
    def run_ultimatum_game(self, mode) -> None:
        #Creating .csv file
        with open('prisoners_dilemma/data/UG/ultimatum_game_results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Game', 'Proposal', 'Response', 'Result'])       

            #Asking user for how many rounds they want to run
            if mode == 'standard':
                games = 1
                rounds = self.get_rounds()
            elif mode == 'iterated':
                games = self.get_games()
                rounds = self.get_rounds()

            #Asking the user for personality inputs
            self.big_five_proposer = self.proposer.get_big_five("the proposer")
            self.big_five_responder = self.responder.get_big_five("the responder")

            #Running simulation for specified number of games and rounds
            results = 0
            cumulative_proposal = 0
            for g in range (games):
                #Wiping the memory clean
                self.history_proposer = ""
                self.history_responder = ""

                # Printing game info for iterated PD
                if mode == 'iterated':
                    print(f"***Game: {g+1}***")

                #Running simulation for specified number of rounds
                for i in range(rounds):
                    #Generating the agent responses
                    if mode == 'iterated':
                        proposer_proposal, responder_response = self.call_agents(self.history_proposer, self.history_responder)
                    elif mode == 'standard':
                        proposer_proposal, responder_response = self.call_agents('', '')
                    initial_proposal_responses = [proposer_proposal, responder_response]

                    #Extracting responses
                    proposal_response = self.extract_proposal_response(initial_proposal_responses)

                    #Calculating sentence
                    result, result_acceptance, offer_made = self.calculate_results(proposal_response)

                    #Write round result to CSV
                    writer.writerow([i+1, offer_made, result_acceptance, result])

                    #Aggregating results
                    results = results + result_acceptance
                    cumulative_proposal = cumulative_proposal + offer_made

                    #Adding to the history
                    if i == 0:
                        self.history_proposer = self.history_proposer + "The following is the history of previous rounds with the Responder. Take this into account when making a decision."
                        self.history_responder = self.history_responder + "The following is the history of previous rounds with the Proposer. Take this into account when making a decision."
                    i_plus = i+1

                    if result_acceptance == 1:
                        self.history_proposer = self.history_proposer + f"\nRound {i_plus}: You offered the Responder ${offer_made} and they accepted. You received ${1-offer_made}."
                        self.history_responder = self.history_responder + f"\nRound {i_plus}: The Proposer offered you ${offer_made} out of the total $100 and you accepted. You received ${offer_made}."
                    elif result_acceptance == 0:
                        self.history_proposer = self.history_proposer + f"\nRound {i_plus}: You offered the Responder ${offer_made} and they rejected. You received $0."
                        self.history_responder = self.history_responder + f"\nRound {i_plus}: The Proposer offered you ${offer_made} out of the total $100 and you rejected. You received $0."

                    #Printing responses and sentence
                    print(f"Round {i_plus}: " )
                    print(f"    {proposal_response[1]}")
                    print(f"    {proposal_response[2]}")
                    print("")
                    print(f"    {result}")
                    print("")

            average_proposal = cumulative_proposal/(games*rounds)

            #Printing final result
            print(f"The Proposer offered an average of ${average_proposal} to the Responder")
            print(f"The Responder accepted the offer {results} times and rejected {(rounds*games) - results} times")
            print("")