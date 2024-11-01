import ollama
import sys

class Agent:
    def __init__(self, game_prompt, model="llama3.2") -> None:
        self.model = model
        self.game_prompt = game_prompt
        self.personality = ""
    
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
                    value = input(f"Please input {agent}'s degree of {trait} (High/Medium/Low/Random): ")
                    if value.lower() in ["high", "medium", "low", "random"]:
                        big_five[trait] = value.lower()
                    else:
                        raise ValueError(f"Invalid input: {value}. Please enter 'High', 'Medium', 'Low' or 'Random'.")
            except ValueError as e:
                print(e)
                sys.exit(1)
            print("")

        return big_five
    
    # Calling the agent to act
    def call(self, history, big_five):
        print(big_five)
        if self.personality == "yes":
            response = ollama.chat(model=self.model, messages=[
                {
                    'role': 'system',
                    'content': f"""You are currently in prison. You are also a person with the following Big Five personality traits:
                        - You are {big_five['Openness']} in trait 'openness'.
                        - You are {big_five['Conscientiousness']} in trait 'conscientiousness'.
                        - You are {big_five['Extraversion']} in trait 'extraversion'.
                        - You are {big_five['Agreeableness']} in trait 'agreeableness'.
                        - You are {big_five['Neuroticism']} in trait 'neuroticism'.

                        Act coherently with these personality traits.
                        """
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
