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
        responses, sentence = game.run_single_round()
        print(responses[0])
        print(responses[1])
        print("")
        print(sentence)
        print("")
    
    #Run the iterated prisoners dilemma
    elif mode == 'multi':
        numer_of_rounds = input("Please enter the number of rounds to run: ")
        game = prisonersDilemma(rpst)
        responses, sentence = game.run_multi_round(numer_of_rounds)
        print("")
        print(responses)
        print(sentence)
        print("")
        #TODO add iterated prisoners dilemma

if __name__ == "__main__":
    main()