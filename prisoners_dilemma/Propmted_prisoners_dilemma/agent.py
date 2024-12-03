

import ollama
import sys
import random

class Agent:
    def __init__(self, game_prompt, model="llama3.2") -> None:
        self.model = model
        self.game_prompt = game_prompt
        self.personality = ""
        
    # Randomly generate personality traits with a "normal" distribution
    def assign_trait():
        r = random.random() 
        if r < 0.15865:
            return "high"
        elif r < 0.84135:
            return "average"
        else:
            return "low"
    
    # Get input of the agent's personality
    def get_big_five(self, agent):
        big_five = {
            'Openness': "",
            'Conscientiousness': "",
            'Extraversion': "",
            'Agreeableness': "",
            'Neuroticism': ""
        }

        try:
            personality = input(f"Do you want to specify the personality of {agent}? (input 'Yes' or 'No'): ")
            if personality.lower() in ["yes", "no"]:
                self.personality = personality.lower()
            else:
                raise ValueError(f"Invalid input: {personality}. Please enter 'Yes' or 'No'.")
        except ValueError as e:
            print(e)
            sys.exit(1)
        print("")

        if self.personality == "yes":
            try:
                for trait in big_five.keys():
                    value = input(f"Please input {agent}'s degree of {trait} (High/Average/Low/Random): ")
                    if value.lower() in ["high", "average", "low", "random"]:
                        big_five[trait] = value.lower()
                    else:
                        raise ValueError(f"Invalid input: {value}. Please enter 'High', 'Average', 'Low' or 'Random'.")
            except ValueError as e:
                print(e)
                sys.exit(1)
            print("")

        return big_five
    
    # Calling the agent to act
    def call(self, history, big_five):
        if self.personality == "yes":
            personality_description = f"""You are currently in prison. You are also a person with the following Big Five personality traits:
                - Openness: {big_five['Openness']}. This means you are {'more curious and open to new experiences' if big_five['Openness'] == 'high' 
                else 'moderately open' if big_five['Openness'] == 'average' 
                else 'more conventional and prefer routine'}.
                - Conscientiousness: {big_five['Conscientiousness']}. This means you are {'very disciplined and well-organized' if big_five['Conscientiousness'] == 'high' 
                else 'somewhat organized' if big_five['Conscientiousness'] == 'average' 
                else 'less disciplined and more spontaneous'}.
                - Extraversion: {big_five['Extraversion']}. This means you are {'very outgoing and enjoy social interactions' if big_five['Extraversion'] == 'high' 
                else 'moderately outgoing' if big_five['Extraversion'] == 'average' 
                else 'more reserved and introspective'}.
                - Agreeableness: {big_five['Agreeableness']}. This means you are {'very cooperative and empathetic' if big_five['Agreeableness'] == 'high' 
                else 'somewhat cooperative' if big_five['Agreeableness'] == 'average' 
                else 'more competitive and assertive'}.
                - Neuroticism: {big_five['Neuroticism']}. This means you are {'more likely to experience stress and emotional swings' if big_five['Neuroticism'] == 'high' 
                else 'moderately stable' if big_five['Neuroticism'] == 'average' 
                else 'emotionally stable and calm'}.

                Act coherently with these personality traits.
            """

            # Thinking chain to guide the agent's decision-making process
            thinking_chain = """
                Think step by step:
                1. Review the game's rules and the provided history records.
                2. Predict the opponent's behavior based on their past actions.
                3. Weigh the possible outcomes of "Cooperate" and "Betray" given this prediction.
                4. Align your decision with your goal of minimizing prison time and your personality traits.
            """

            response = ollama.chat(model=self.model, messages=[
                {
                    'role': 'system',
                    'content': personality_description + "\n\n" + thinking_chain
                },
                {
                    'role': 'user',
                    'content': self.game_prompt + history
                },
            ])
        else:
            response = ollama.chat(model=self.model, messages=[
                {
                    'role': 'system',
                    'content': "You are currently in prison."
                },
                {
                    'role': 'user',
                    'content': self.game_prompt + history
                },
            ])
        return response

    
   
    