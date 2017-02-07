import numpy as np
import gym
from gym import spaces
from gym.utils import seeding


class Environment(gym.Env):
    def __init__(self, discrete, game_class, seed, observations_count, actions_in_phases):
        self.game_class = game_class
        self.game_instance = None
        self.state = None
        self.actions_in_phases = actions_in_phases
        self.last_phase = 0
        self.done = False

        actions_total = sum(actions_in_phases)
        if discrete:
            self.observation_space = spaces.Discrete(n=observations_count)
            self.action_space = spaces.Discrete(n=actions_total)
        else:
            self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(observations_count,))
            self.action_space = spaces.Box(low=-1, high=1, shape=(actions_total,))

        self._seed(seed)
        self.reset()
        self.viewer = None
        self._configure()

    def _step(self, action):
        """
        Performs a single step in the game.
        :param action: Action to make.
        :return: By Gym-interface, returns observation (new state), reward, done, info
        """

        # If game is already completed (but rest of the games in the batch are not...)
        if self.done:
            return self.state, 0, True, self.game_instance.score

        # Need to determine proper game phase and use only specific action subset
        if len(self.actions_in_phases) > 1:
            print(self.actions_in_phases)
            begin = sum(self.actions_in_phases[:self.last_phase])
            end = begin + self.actions_in_phases[self.last_phase]
            action = action[begin:end]

        action_string = ""
        for a in action:
            action_string += str(a) + " "

        new_state, self.last_phase, reward, done = self.game_instance.step(action_string)
        self.state = new_state
        self.done = done
        return self.state, reward, done, self.game_instance.score

    def _configure(self, display=None):
        self.display = display

    def _seed(self, seed=None):
        self.np_random, s = seeding.np_random(seed)
        return s

    def _reset(self):
        if self.game_instance != None:
            self.game_instance.finalize()
        model = None
        game_batch = 1
        seed = np.random.randint(0, 2 ** 16)
        self.game_instance = self.game_class(model, game_batch, seed)
        self.done = False
        self.last_phase = 0
        self.state, _ = self.game_instance.init_process()  # First state of the game
        return self.state

    def _render(self, mode='human', close=False):
        pass

    def _close(self):
        self.shut_down()

    def shut_down(self):
        self.game_instance.finalize()
