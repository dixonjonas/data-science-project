import ollama
import csv
import sys
from agent import Agent

class TrustGame:
    """
    This class implements an iterative Trust Game with Big Five personality simulation.
    Agent1 decides how much to invest (0-10), the investment is then tripled and given to Agent2,
    and Agent2 decides how much to return to Agent1 (0 up to the received amount).
    Both players aim to maximize their own total earnings.
    """

    def __init__(self):
        # Initialize conversation histories for Agent1 and Agent2
        self.history_agent1 = ""
        self.history_agent2 = ""

        # Base prompts for Agent1 and Agent2
        self.agent1_prompt = (
            "You are Agent 1 in the Trust Game. You have a total of $10. "
            "You can decide to invest any amount (between $0 and $10) to Agent 2. "
            "Any amount you invest will be tripled and given to Agent 2. "
            "Agent 2 will then decide how much of the tripled amount to return to you. "
            "Your goal is to maximize your total earnings. "
            "Your output must be an integer between 0 and 10, representing the amount you want to invest. **Do not add any text besides the integer itself**"
        )

        self.agent2_prompt = (
            "You are Agent 2 in the Trust Game. Agent 1 has decided to invest some amount of money in you. "
            "The amount you receive is three times what Agent 1 invested. You can decide how much of this "
            "tripled amount to return to Agent 1. Your goal is to maximize your total earnings while "
            "considering the actions and trust of Agent 1. "
            "Your output must be an integer between 0 and the amount you received. **Do not add any text besides the integer itself**"
        )

        # Create Agent instances
        self.agent1 = Agent(self.agent1_prompt)
        self.agent2 = Agent(self.agent2_prompt)

        # Prepare dictionaries to store the Big Five personality traits
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

  
    def get_mode(self):
        try:
            print("")
            mode = input("Please enter 'one-shot' for the standard (one-shot) trust game or 'iterated' for the iterated trust game: ")
            print("")
            if mode.lower() == "one-shot" or mode.lower() == "iterated":
                return mode.lower()
            else:
                raise ValueError(f"Invalid input: {mode}. Please enter 'one-shot' or 'iterated'.")
        except ValueError as e:
            print(e)
            sys.exit(1)
            
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
        # Create local copies of the Big Five dictionaries for each agent
        # This step ensures we integrate either user-defined or random traits
        big_five_dict_agent1 = {}
        big_five_dict_agent2 = {}

        # Assign traits for Agent1
        for trait in self.big_five_agent1:
            if self.big_five_agent1[trait] != 'random':
                big_five_dict_agent1[trait] = self.big_five_agent1[trait]
            else:
                big_five_dict_agent1[trait] = self.assign_trait()  # or your logic for random assignment

        # Assign traits for Agent2
        for trait in self.big_five_agent2:
            if self.big_five_agent2[trait] != 'random':
                big_five_dict_agent2[trait] = self.big_five_agent2[trait]
            else:
                big_five_dict_agent2[trait] = self.assign_trait()

        # Agent 1 decides how much to invest
        while True:
            agent1_response = self.agent1.call(
                history_agent1,
                big_five_dict_agent1,
                ""
            )
            agent1_investment_str = agent1_response['message']['content'].strip()
            
            print("DEBUG: Agent1 raw output ->", repr(agent1_investment_str))

            try:
                agent1_investment = int(agent1_investment_str)
                if 0 <= agent1_investment <= 10:
                    break
            except ValueError:
                print("DEBUG: Could not parse as int, going to loop again.")
                pass

        # Agent 2 decides how much to return
        received_amount = agent1_investment * 3
        while True:
            agent2_response = self.agent2.call(
                history_agent2,
                big_five_dict_agent2,
                f"You have received {received_amount} from Agent1."
            )
            agent2_return_str = agent2_response['message']['content'].strip()

            try:
                agent2_return = int(agent2_return_str)
                if 0 <= agent2_return <= received_amount:
                    break
            except ValueError:
                pass

        return agent1_investment, agent2_return

    def calculate_results(self, investment, returned_amount):
        agent1_earnings = 10 - investment + returned_amount
        agent2_earnings = (investment * 3) - returned_amount
        result_str = f"Agent 1 invested ${investment}, and Agent 2 returned ${returned_amount}."
        return result_str, agent1_earnings, agent2_earnings

    def run_trust_game(self, mode):
        print("Now, let's configure the Big Five personality traits for each Agent.\n"
              "Please type a specific value (e.g., 'High', 'Medium', 'Low') or 'random' for each trait.\n")

        self.big_five_agent1 = self.agent1.get_big_five("Agent 1")  # get big five traits for Agent1
        self.big_five_agent2 = self.agent2.get_big_five("Agent 2")  # get big five traits for Agent2

        with open('trust_game_results.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Round', 'Agent 1 Investment', 'Agent 2 Return', 'Result', 'Agent 1 Earnings', 'Agent 2 Earnings'])

            # Determine how many rounds to run based on the chosen mode
            if mode == "one-shot":
                rounds = 1
            elif mode == "iterated":
                rounds = self.get_rounds()
            else:
                raise ValueError("Invalid mode. Choose either 'one-shot' or 'iterated'.")

            agent1_total_score = 0
            agent2_total_score = 0

            # Run the specified number of rounds
            for i in range(rounds):
                # If it is iterated, we pass the accumulated history to the Agents
                # If it is one-shot, we do not use prior history
                if mode == "iterated":
                    investment, returned_amount = self.call_agents(self.history_agent1, self.history_agent2)
                else:  # 'one-shot' case
                    investment, returned_amount = self.call_agents("", "")

                # Calculate the result for each round
                result_str, agent1_score, agent2_score = self.calculate_results(investment, returned_amount)

                # Write data to CSV
                writer.writerow([
                    i + 1,
                    investment,
                    returned_amount,
                    result_str,
                    agent1_score,
                    agent2_score
                ])

                # Print round outcome to console
                print(f"Round {i + 1}: {result_str}")
                print(f"Agent 1 total this round: {agent1_score}, Agent 2 total this round: {agent2_score}\n")

                # Update total scores
                agent1_total_score += agent1_score
                agent2_total_score += agent2_score

                # Update the conversation history for iterated mode
                if mode == "iterated":
                    self.history_agent1 += (
                        f"Round {i + 1}: You invested ${investment}. "
                        f"Agent 2 returned ${returned_amount}. "
                        f"{result_str}\n"
                    )
                    self.history_agent2 += (
                        f"Round {i + 1}: Agent 1 invested ${investment}. "
                        f"You returned ${returned_amount}. "
                        f"{result_str}\n"
                    )

            # Print final scores after all rounds
            print("\nFinal Scores:")
            print(f"Agent 1: {agent1_total_score} points")
            print(f"Agent 2: {agent2_total_score} points")

            # If it's one-shot, indicate the game has ended
            if mode == "one-shot":
                print("\nThis was a one-shot game. No further rounds will be played.")


