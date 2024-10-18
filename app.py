import ollama
import json
import os
import time
from agent import Agent
from prisoners_dilemma import prisonersDilemma

def main():
    #Initializing rewards
    rpst = ['1','2','3','0']

    #Asking the user to set the mode
    mode = input("Please enter 'single' for normal prisoners dilemma or 'multi' for iterated prisoners dilemma: ")

    #Run the normal prisoners dilemma
    if mode == 'single':
        game = prisonersDilemma(rpst)
        responses = game.run_single_round()
        print(responses)
    
    #Run the iterated prisoners dilemma
    elif mode == 'multi':
        numer_of_rounds = input("Please enter the number of rounds to run: ")
        game = prisonersDilemma(rpst)
        responses = game.run_multi_round(numer_of_rounds)
        print(responses)

if __name__ == "__main__":
    main()