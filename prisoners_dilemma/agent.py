import ollama
import sys

class Agent:
    def __init__(self, game_prompt, model = "llama3.2") -> None:
        self.model = model
        self.game_prompt = game_prompt
        self.big_five = {}
    
    #Get input of the agents personality
    def get_big_five(self, agent) -> None:
        self.big_five = {
            'Openness': "",
            'Conscientiousness': "",
            'Extraversion': "",
            'Agreeableness': "",
            'Neuroticism': ""
        }

        #TODO fix this try/except block
        try:
            for trait, value in self.big_five.items():
                value = input(f"Please input {agent}'s degree of {trait} (High/Low): ")
                if value.lower() == "high" or value.lower() == "low":
                    self.big_five[trait] = value.lower()
                else:
                    raise ValueError(f"Invalid input: {value}. Please enter 'High' or 'Low'.")
        except ValueError as e:
            print(e)
            sys.exit(1)
        print("")
    
    #Calling the agent to act
    def call(self, history):
        response = ollama.chat(model=self.model, messages=[
            {
                'role': 'user',
                'content': f"""You are a person with the following Big Five personality traits:
                    You are {self.big_five['Openness']} in trait 'openness'.
                    You are {self.big_five['Conscientiousness']} in trait 'conscientiousness'.
                    You are {self.big_five['Extraversion']} in trait 'extraversion'.
                    You are {self.big_five['Agreeableness']} in trait 'agreeableness'.
                    You are {self.big_five['Neuroticism']} in trait 'neuroticism'.
                    - Act coherently with your personality traits.
                    """ + self.game_prompt + history,
            },
        ])
        return response