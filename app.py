import ollama
from agent import Agent
from prisoners_dilemma import prisonersDilemma

def main():
    #Initializing rewards
    rpst = ['1','2','3','0']

    #Asking the user to set the mode
    mode = prisonersDilemma.get_mode()

    #Run the prisoners dilemma
    game = prisonersDilemma(rpst)
    game.run_prisoners_dilemma(mode)

if __name__ == "__main__":
    main()