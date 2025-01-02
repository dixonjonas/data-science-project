import csv
import sys
from agent import Agent

class BattleOfSexesGame:
    def __init__(self):
        self.history_agent1 = ""
        self.history_agent2 = ""

        self.agent1_prompt = """You are Agent 1 in the Battle of the Sexes game. You have two choices: 'A' and 'B'. 
        You prefer choice 'A', and if both you and Agent 2 choose 'A', you will receive 2 points, and Agent 2 will receive 1 point. 
        However, Agent 2 prefers choice 'B'. If both of you choose 'B', you will receive 1 point, and Agent 2 will receive 2 points. 
        If you and Agent 2 choose different options, you will both receive 0 points. 

        Your goal is to maximize your points while considering the preferences and possible actions of Agent 2. 
        Your output must be either 'A' or 'B' and nothing else. Any other response will be treated as invalid."""

        self.agent2_prompt = """You are Agent 2 in the Battle of the Sexes game. You have two choices: 'A' and 'B'. 
        You prefer choice 'B', and if both you and Agent 1 choose 'B', you will receive 2 points, and Agent 1 will receive 1 point. 
        However, Agent 1 prefers choice 'A'. If both of you choose 'A', you will receive 1 point, and Agent 1 will receive 2 points. 
        If you and Agent 1 choose different options, you will both receive 0 points. 

        Your goal is to maximize your points while considering the preferences and possible actions of Agent 1. 
        Your output must be either 'A' or 'B' and nothing else. Any other response will be treated as invalid."""



        self.agent1 = Agent(self.agent1_prompt)
        self.agent2 = Agent(self.agent2_prompt)

        self.big_five_agent1 = {
            'Openness': "",
            'Conscientiousness': "",
            'Extraversion': "",
            'Agreeableness': "",
            'Neuroticism': ""
        }

        self.big_five_agent2 = {
            'Openness': "",
            'Conscientiousness': "",
            'Extraversion': "",
            'Agreeableness': "",
            'Neuroticism': ""
        }

    def get_rounds(self):
        try:
            rounds = int(input("Enter the number of rounds to simulate: "))
            if rounds <= 0:
                raise ValueError("Number of rounds must be positive.")
            return rounds
        except ValueError:
            print("Invalid input! Please enter a positive integer.")
            sys.exit(1)

    def call_agents(self, history_agent1, history_agent2):
        agent1_choice = ""
        agent2_choice = ""

        if history_agent1 == "" and history_agent2 == "":
            self.big_five_agent1 = {k: v if v not in ['random', ''] else Agent.assign_trait() for k, v in self.big_five_agent1.items()}
            self.big_five_agent2 = {k: v if v not in ['random', ''] else Agent.assign_trait() for k, v in self.big_five_agent2.items()}

        while True:
            agent1_choice = self.agent1.call(history_agent1, self.big_five_agent1, '')['message']['content'].strip().upper()
            if agent1_choice in ['A', 'B']:
                break

        while True:
            agent2_choice = self.agent2.call(history_agent2, self.big_five_agent2, '')['message']['content'].strip().upper()
            if agent2_choice in ['A', 'B']:
                break

        return agent1_choice, agent2_choice

    def calculate_results(self, choices):
        agent1_choice, agent2_choice = choices

        if agent1_choice == agent2_choice:
            if agent1_choice == 'A':
                return "Both chose A. Agent 1 gets 2 points, Agent 2 gets 1 point.", 2, 1
            else:
                return "Both chose B. Agent 1 gets 1 point, Agent 2 gets 2 points.", 1, 2
        else:
            return "Choices differ. Both get 0 points.", 0, 0
        
        #Set the mode of the battle of sexes
    def get_mode():
        try:
            print("")
            mode = input("Please enter 'one-shot' for the standard (one-shot) battle of sexes or 'iterated' for the iterated battle of sexes: ")
            print("")
            if mode.lower() == "one-shot" or mode.lower() == "iterated":
                return mode.lower()
            else:
                raise ValueError(f"Invalid input: {mode}. Please enter 'one-shot' or 'iterated'.")
        except ValueError as e:
            print(e)
            sys.exit(1)


    def run_battle_of_sexes(self, mode):
        # Open a CSV file to log results
        with open('battle_of_sexes_results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Round', 'Agent 1 Choice', 'Agent 2 Choice', 'Result', 'Agent 1 Score', 'Agent 2 Score', 'Agent 1 Personality', 'Agent 2 Personality'])

            # Determine the number of rounds based on the mode
            if mode == "one-shot":
                rounds = 1
            elif mode == "iterated":
                rounds = self.get_rounds()
            else:
                raise ValueError("Invalid mode. Choose either 'one-shot' or 'iterated'.")

            # Get personality traits for both agents
            self.big_five_agent1 = self.agent1.get_big_five("Agent 1")
            self.big_five_agent2 = self.agent2.get_big_five("Agent 2")

            # Initialize scores
            agent1_total_score = 0
            agent2_total_score = 0

            # Loop through each round
            for i in range(rounds):
                # Call agents to get their choices
                if mode == "iterated":
                    choices = self.call_agents(self.history_agent1, self.history_agent2)
                elif mode == "one-shot":
                    choices = self.call_agents("", "")  # No history for one-shot

                # Calculate results based on choices
                result, agent1_score, agent2_score = self.calculate_results(choices)

                # Write the results of the round to the CSV
                writer.writerow([i + 1, choices[0], choices[1], result, agent1_score, agent2_score, self.big_five_agent1, self.big_five_agent2])

                # Update total scores
                agent1_total_score += agent1_score
                agent2_total_score += agent2_score

                # Update histories (only relevant for iterated mode)
                if mode == "iterated":
                    self.history_agent1 += f"Round {i + 1}: You chose {choices[0]}. Agent 2 chose {choices[1]}. {result}\n"
                    self.history_agent2 += f"Round {i + 1}: You chose {choices[1]}. Agent 1 chose {choices[0]}. {result}\n"

                # Print results of the round
                print(f"Round {i + 1}: {result}")

            # Print final scores after all rounds
            print("\nFinal Scores:")
            print(f"Agent 1: {agent1_total_score} points")
            print(f"Agent 2: {agent2_total_score} points")

            # If it's a one-shot game, provide an explicit summary
            if mode == "one-shot":
                print("\nThis was a one-shot game. No further rounds will be played.")


