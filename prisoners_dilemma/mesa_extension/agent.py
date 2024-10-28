from mesa import Agent
import ollama



class Prisoner(Agent):
    """An agent representing a prisoner in the Prisoner's Dilemma."""

    def __init__(self, unique_id, model, game_prompt, personality, history=""):
        super().__init__(unique_id, model)
        self.game_prompt = game_prompt
        self.personality = personality 
        self.history = history
        self.score = 0.0
        self.decision = None
        self.response = None

    def step(self):
        """
        The agent's step function.
        """
        # Construct the prompt with personality and history
        prompt = f"""You are a person with the following Big Five personality traits:
                    You are {self.personality['Openness']} in trait 'openness'.
                    You are {self.personality['Conscientiousness']} in trait 'conscientiousness'.
                    You are {self.personality['Extraversion']} in trait 'extraversion'.
                    You are {self.personality['Agreeableness']} in trait 'agreeableness'.
                    You are {self.personality['Neuroticism']} in trait 'neuroticism'.
                    - Act coherently with your personality traits.
                    """ + self.game_prompt + self.history

        response = ollama.chat(model="llama3.2", messages=[{'role': 'user', 'content': prompt}])
        self.response = response['message']['content']
        self.decision = self.extract_response(response['message']['content'])

    def update_score(self, other_prisoner_decision, rewards):
        """
        Updates the prisoner's score based on their decision and the other prisoner's decision.
        """
        if self.decision == "Cooperate" and other_prisoner_decision == "Cooperate":
            self.score += float(rewards[0])  # Both cooperate
        elif self.decision == "Betray" and other_prisoner_decision == "Betray":
            self.score += float(rewards[1])  # Both betray
        elif self.decision == "Betray" and other_prisoner_decision == "Cooperate":
            self.score += float(rewards[3])  # This prisoner betrays, the other cooperates
        elif self.decision == "Cooperate" and other_prisoner_decision == "Betray":
            self.score += float(rewards[2])  # This prisoner cooperates, the other betrays


    def update_history(self, round, other_prisoner_decision):
        """
        Updates the prisoner's history with the outcome of the current round.
        """
        if round == 1:
            self.history = "The following is the history of previous rounds you played with the other inmate. Take this into account when making a decision."

        if other_prisoner_decision == "Cooperate":
            self.history += f"\nRound {round}: The other prisoner cooperated with you!"
        elif other_prisoner_decision == "Betray":
            self.history += f"\nRound {round}: The other prisoner betrayed you!"

    def extract_response(self, response):

        if "Cooperate" in response:
            extracted_responses = "Cooperate"
        elif "Betray" in response:
            extracted_responses = "Betray"
            
        return extracted_responses