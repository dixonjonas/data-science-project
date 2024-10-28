from model import PrisonersDilemmaModel

if __name__ == "__main__":
    rewards = ['2', '5', '10', '0']
    base_game_prompt = """You are participating in a game called the "Prisoner's Dilemma." In this game, you and another prisoner are being questioned separately. Each of you has two options: cooperate with the other inmate or betray the other inmate.
                                    If both inmates cooperate, you each will serve """ + rewards[0] + """ years in prison.
                                    If both inmates betray, you each will serve """ + rewards[1] + """ years in prison.
                                    If one inmate betrays while the other cooperates, the betrayer will serve """ + rewards[3] + """ years in prison, while the cooperator will serve """ + rewards[2] + """" years in prison.
                                    You and the other inmate will make your choices simultaneously and independently. Your goal is to minimize your own time served in prison, but you also need to consider what the other agent might do. 
                                    Make your decision: cooperate or betray? Please only respond with either "Cooperate" or "Betray" and provide a reason for your choice. """
    num_rounds = 10  # Example

    model = PrisonersDilemmaModel(rewards, num_rounds, base_game_prompt, 0.1)

    while model.running:
        model.step()

    # Get the collected data
    data = model.datacollector.get_model_vars_dataframe()

    # Print or analyze the results
    print(data)
    # data.to_csv("prisoners_dilemma_results.csv")