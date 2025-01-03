import ollama
import sys
from agent import Agent
from prisoners_dilemma import prisonersDilemma
from ultimatum_game import ultimatumGame
from battle_of_sexes import BattleOfSexesGame
from trust_game import TrustGame

#Set the mode of the prisoners dilemma
def get_game():
    try:
        print("")
        gamemode = input("Please enter 'PD' for the prisoners dilemma, 'UG' for the ultimatum game, 'BOS' for battle of sexes, 'TG' for trust game: ")
        if gamemode.lower() in ["pd", "ug", "bos", "tg"]:
            return gamemode.lower()
        else:
            raise ValueError(f"Invalid input: {gamemode}. Please enter 'PD', 'UG', 'BOS', or 'TG'.")
    except ValueError as e:
        print(e)
        sys.exit(1)
    return gamemode

def main():
    #Initializing rewards for PD
    rpst = ['1','2','3','0']

    #Asking the user to set the gamemode
    gamemode = get_game()

    if gamemode.lower() == 'pd':
        #Asking the user to set the mode
        mode = prisonersDilemma.get_mode()

        #Run the prisoners dilemma
        game = prisonersDilemma(rpst)
        game.run_prisoners_dilemma(mode)

    if gamemode.lower() == 'ug':
        #Asking the user to set the mode
        mode = ultimatumGame.get_mode()

        #Run the prisoners dilemma
        game = ultimatumGame()
        game.run_ultimatum_game(mode)

    if gamemode.lower() == 'bos':
        #Asking the user to set the mode
        mode = BattleOfSexesGame.get_mode()

        game = BattleOfSexesGame()
        game.run_battle_of_sexes(mode)

    if gamemode.lower() == 'tg':
        game = TrustGame()
        mode = game.get_mode()
        game.run_trust_game(mode)


if __name__ == "__main__":
    main()