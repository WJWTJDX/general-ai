import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os, json

import games
import time
import utils.miscellaneous
from models.mlp import MLP
from models.echo_state_network import EchoState
from models.random import Random
from models.learned_dqn import LearnedDQN
from models.learned_ddpg import LearnedDDPG


def bar_plot(values, evals, game):
    fig, ax = plt.subplots(figsize=(6, 7))

    bar_width = 0.3
    opacity = 0.5

    for index, (name, value) in enumerate(values):
        rects = plt.bar(index, value, bar_width,
                        alpha=opacity,
                        color='b',
                        label=name,
                        align='center')
        autolabel(rects, ax)

    ylim = get_y_lim_for_game(game)

    plt.ylim([0, ylim])
    plt.gca().axes.set_xticklabels([])
    plt.ylabel('AVG fitness')
    plt.title('Model comparison - {} runs - {}'.format(evals, game))

    x = np.arange(len(values))
    ax.set_xticks(x)
    ax.set_xticklabels([name for (name, _) in values])

    plt.tight_layout()
    plt.savefig('comparison.png')


def get_y_lim_for_game(game):
    ylim = None
    if game == "alhambra":
        ylim = 200
    if game == "torcs":
        ylim = 3000
    if game == "mario":
        ylim = 1.2
    if game == "2048":
        ylim = 5000
    return ylim


def autolabel(rects, ax):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                '{}'.format(float(height)),
                ha='center', va='bottom')


def eval(game, evals, model):
    parameters = [model, evals, np.random.randint(0, 2 ** 16)]
    values = []
    game_instance = utils.miscellaneous.get_game_instance(game, parameters)

    results = game_instance.run(advanced_results=True)
    for i, r in enumerate(results):
        if i > 0:
            values.append(("original#{}".format(i), r))
        else:
            values.append((model.get_name(), r))
    return values


def compare_models(game, evals, *args):
    print("Comparing models:")
    values = []
    for model in args:
        print(model.get_name())
        values += eval(game=game, evals=evals, model=model)
    bar_plot(values, evals, game)


def eval_mario_winrate(model, evals, level, vis_on):
    """
    Evaluates mario winrate on specified level.
    :param model:
    :param evals:
    :param level: gombas or spikes
    :param vis_on:
    :return:
    """
    game_instance = games.mario.Mario(model, evals, np.random.randint(0, 2 ** 16), level=level, vis_on=vis_on,
                                      use_visualization_tool=True)
    results = game_instance.run(advanced_results=True)
    print("Mario winrate: {}".format(results))


def run_torcs_vis_on(model, evals):
    game_instance = games.torcs.Torcs(model, evals, np.random.randint(0, 2 ** 16), vis_on=True)
    print("Torcs visualization started.")
    results = game_instance.run(advanced_results=True)


def run_2048_extended(model, evals):
    print("Game 2048 with extended logs started.")
    game_instance = games.game2048.Game2048(model, evals, np.random.randint(0, 2 ** 16))
    results = game_instance.run(advanced_results=True)


def run_random_model(game, evals):
    print("Generating graph of 'random' model for game {}.".format(game))
    results = []
    t = time.time()
    for i in range(evals):
        if time.time() - t > 1 or i == evals - 1:
            print("{}/{}".format(i + 1, evals))
            t = time.time()
        parameters = [Random(game), 1, np.random.randint(0, 2 ** 16)]
        game_instance = utils.miscellaneous.get_game_instance(game, parameters)
        result = game_instance.run()
        results.append(result)

    x = range(0, evals)
    # plt.plot(x, results, 'b', x, [np.mean(results) for _ in results], 'r--')
    plt.scatter(x, results, cmap='b')
    plt.plot([np.mean(results) for _ in results], 'r--')
    plt.title("Random - game: {} - Average score: {}".format(game, np.mean(results)))
    plt.ylim(0, get_y_lim_for_game(game))
    plt.xlim(0, evals)
    plt.xlabel("Evals")
    plt.ylabel("Score")
    plt.savefig("random_model_{}.png".format(game))


def eval_alhambra_winrate(model, evals):
    print("Evaluating Alhambra winrate.")
    results = []
    wins = 0
    for i in range(evals):
        print("{}/{}".format(i + 1, evals))
        game_instance = games.alhambra.Alhambra(model, 1, np.random.randint(0, 2 ** 16))
        result = game_instance.run(advanced_results=True)
        if np.argmax(result) == 0:
            wins += 1
    print("Alhambra winrate: {} ({}/{})".format(wins / evals, wins, evals))


def run_model_evaluator():
    """
    Used for evaluating learned models, to benchmark them and get avg results.
    For example, to run 1000 games and plot results.
    """

    np.random.seed(930615)
    game = "2048"
    evals = 1000
    # run_random_model("2048", 1000)
    # file_name = "../../Experiments/ESN+evolution_algorithm/2048/logs_2017-01-27_00-31-41/best/best_0.json"
    # file_name = "../../Controller/logs/2048/mlp/logs_2017-02-04_00-17-33/best/best_0.json"
    # file_name = "C:/Users/Jan/Desktop/lab_logs/master/logs/mario/mario new/mlp/logs_2017-02-20_10-55-14/best/best_0.json"
    # file_name = "../../Experiments/MLP+differential_evolution/mario/logs_2017-02-04_00-30-52/last/last_0.json"
    # file_name = "../../Experiments/MLP+evolution_algorithm/alhambra/logs_2017-01-19_00-32-53/best/best_0.json"
    # file_name = "../../Experiments/MLP+evolution_strategy/2048/logs_2017-02-21_17-30-47/best/best_0.json"
    # file_name = "../../Controller/logs/mario/mlp/logs_2017-02-21_00-23-53/best/best_0.json"
    # logdir = "../../Controller/logs/torcs/deep_deterministic_gradient_policy/logs_2017-02-12_01-22-16"
    logdir = "D:/Github/general-ai/Experiments/reinforcement_learning/2048/logs_2017-04-18_18-25-40"
    # logdir = "D:/Github/general-ai/Controller/logs/mario/dqn/logs_2017-04-19_16-26-07"

    # esn = EchoState.load_from_file(file_name, game)
    # random = Random(game)
    # mlp = MLP.load_from_file(file_name, game)
    # eval_alhambra_winrate(Random(game), evals)
    dqn = LearnedDQN(logdir)

    # ddpg = LearnedDDPG(logdir)

    # run_random_model(game, evals)
    run_2048_extended(dqn, evals)

    # eval_mario_winrate(model=dqn, evals=evals, level="gombas", vis_on=True)
    # compare_models(game, evals, Random(game))
    # run_torcs_vis_on(model=mlp, evals=evals)


def run_plot_creator():
    """
    Used for creating some graphs, plots, etc...
    """

    dir_name = "..."
    game = "2048"

    with open(os.path.join(dir_name, "metadata.json"), "r") as f:
        metadata = json.load(f)

    data = np.loadtxt(os.path.join(dir_name, "logbook.txt"), skiprows=1)
    episodes = data[:, 0]
    scores = data[:, 2]

    plt.figure()
    plt.plot(episodes, scores, label="score")

    plt.xlabel("Episode")
    plt.ylabel("Score")
    plt.xlim([0, len(episodes)])
    plt.legend(loc="lower right")
    plt.title("GAME: {}\n{}".format(game, metadata, fontsize=10))
    plt.savefig("plot.png")


if __name__ == '__main__':
    run_model_evaluator()
    # run_plot_creator()
