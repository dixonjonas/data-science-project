from mesa import Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from agent import Prisoner  # Import your Prisoner agent class
import random

def get_round_data(model):
    """
    Collects data for the current round.
    """
    return {
        "Round": model.current_round,
        "Prisoner 1 Response": model.prisoner1.decision,
        "Prisoner 2 Response": model.prisoner2.decision,
        "Prisoner 1 Score": model.prisoner1.score,
        "Prisoner 2 Score": model.prisoner2.score,
        "Prisoner 1 LLM Response": model.prisoner1.response,
        "Prisoner 2 LLM Response": model.prisoner2.response,
        "Probability of Game Ending": model.discount_factor
    }

class PrisonersDilemmaModel(Model):
    """A model representing the Prisoner's Dilemma game."""

    def __init__(self, rewards, num_rounds, base_game_prompt, discount_factor=None):
        super().__init__()
        self.num_agents = 2
        self.schedule = RandomActivation(self)
        self.num_rounds = num_rounds
        self.current_round = 1
        self.base_game_prompt = base_game_prompt
        self.rewards = rewards
        self.discount_factor = discount_factor
        self.running = True
        self.datacollector = DataCollector(
            model_reporters={"Data": lambda m: get_round_data(m)},
            agent_reporters={"Score": lambda a: a.score}
        )

        # Create two Prisoner agents with their personalities
        self.prisoner1 = Prisoner(1, self, self.base_game_prompt, personality={
                                                    "Openness": "medium",      
                                                    "Conscientiousness": "high", 
                                                    "Extraversion": "low",     
                                                    "Agreeableness": "medium",   
                                                    "Neuroticism": "low"      
                                                    },
                                                    )  
        self.prisoner2 = Prisoner(2, self, self.base_game_prompt, personality={
                                                    "Openness": "low",      
                                                    "Conscientiousness": "high", 
                                                    "Extraversion": "low",     
                                                    "Agreeableness": "medium",   
                                                    "Neuroticism": "low"      
                                                    })  

        self.schedule.add(self.prisoner1)
        self.schedule.add(self.prisoner2)

    def step(self):
        """
        The model's step function.
        """

        # Update the game prompt with the current discount factor for EACH agent
        if self.discount_factor is not None:
            self.prisoner1.game_prompt = self.generate_prompt(self.discount_factor)
            self.prisoner2.game_prompt = self.generate_prompt(self.discount_factor)

        self.schedule.step()  

        # Determine the outcome and update scores
        self.prisoner1.update_score(self.prisoner2.decision, self.rewards)
        self.prisoner2.update_score(self.prisoner1.decision, self.rewards)

        # Update histories for iterated games (if needed)
        self.prisoner1.update_history(self.current_round, self.prisoner2.decision)
        self.prisoner2.update_history(self.current_round, self.prisoner1.decision)

        self.datacollector.collect(self) 

        self.current_round += 1

        # Game ending condition:
        if self.discount_factor is None:
            # Fixed number of rounds mode
            if self.current_round > self.num_rounds:
                self.running = False
        else:
            # Discount factor mode
            if random.random() < self.discount_factor:
                self.running = False 

            # Increase the discount factor for the next round
            #self.discount_factor = min(self.discount_factor , 1.0)  # Cap at 1.0

    
    def generate_prompt(self, discount_factor):
        """
        Generates the complete game prompt with the personality traits 
        and the explicit discount factor statement.
        """
        prompt = f"""{self.base_game_prompt}

                    Important: There is a **{discount_factor:.0%} chance** that the game will end after this round. 
                    Take this into account when making a decision.
                    Make your decision: cooperate or betray?"""
        return prompt