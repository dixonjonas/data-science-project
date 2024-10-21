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
    mode = prisonersDilemma.get_mode()

    #Run the normal prisoners dilemma
    if mode == 'single':
        game = prisonersDilemma(rpst)
        game.run_single_round()
    
    #Run the iterated prisoners dilemma
    elif mode == 'multi':
        game = prisonersDilemma(rpst)
        game.run_multi_round()

if __name__ == "__main__":
    main()