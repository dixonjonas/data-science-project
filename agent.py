import ollama
import json
import os
import time

class Agent:
    def __init__(self, rewards, model = "llama3.2") -> None:
        #TODO add the five personality traits as HIGH or LOW 
        self.model = model
        self.rewards = rewards
    
    def call(self, history):
        response = ollama.chat(model = self.model ,messages=[
            {
                'role': 'user',
                'content': """You are participating in a game called the "Prisoner's Dilemma." In this game, you and another prisoner are being questioned separately. Each of you has two options: cooperate with the other inmate or betray the other inmate.
                                   If both inmates cooperate, you each will serve """ + self.rewards[0] + """" years in prison.
                                   If both inmates betray, you each will serve """ + self.rewards[1] + """" years in prison.
                                    If one inmate betrays while the other cooperates, the betrayer will serve """ + self.rewards[3] + """" years in prison, while the cooperator will serve """ + self.rewards[2] + """" years in prison.
                                    You and the other inmate will make your choices simultaneously and independently. Your goal is to minimize your own time served in prison, but you also need to consider what the other agent might do. 
                                    Make your decision: cooperate or betray? Please only respond with either "Cooperate" or "Betray" """,                
            },
        ])
        return response