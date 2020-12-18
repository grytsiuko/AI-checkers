import random

from heuristics.generic_heuristic import GenericHeuristic
from training import random_generic_heuristic_weights, test_heuristics, random_pair


class GeneticAlgorithm:
    MAX_POPULATIONS = 100
    MAX_INDIVIDUALS = 16
    MUTATION_TIMES = 1

    def __init__(self):
        assert self.MAX_INDIVIDUALS % 4 == 0
        self.weights_list = self._init_weights()
        self.current_population = 0

    def start(self):
        while self.current_population < self.MAX_POPULATIONS:
            self._run_population()
            self.current_population = self.current_population + 1
        print("\n\n\n### RESULT ###")
        for weights in self.weights_list:
            print(weights)

    def _run_population(self):
        print(f"### POPULATION {self.current_population} ###")
        for weights in self.weights_list:
            print(weights)
        print()

        # get survivals
        random.shuffle(self.weights_list)
        survived_list = self._get_half_best(self.weights_list)
        assert len(survived_list) == self.MAX_INDIVIDUALS // 2

        print(f"Survived")
        for weights in survived_list:
            print(weights)

        next_population = []

        # crossover
        random.shuffle(survived_list)
        for i in range(0, self.MAX_INDIVIDUALS // 2, 2):
            weights1 = survived_list[i]
            weights2 = survived_list[i + 1]
            new_weights1, new_weights2 = self._crossover_weights(weights1, weights2)
            next_population += [weights1, weights2, new_weights1, new_weights2]
        assert len(next_population) == self.MAX_INDIVIDUALS

        print(f"Crossed")
        for weights in next_population:
            print(weights)

        # mutations
        for i in range(0, self.MAX_INDIVIDUALS):
            curr = next_population[i]
            for k in range(0, (2 ** self.MUTATION_TIMES) - 1):
                next_population.append(self._mutate_weights(curr))
        assert len(next_population) == self.MAX_INDIVIDUALS * (2 ** self.MUTATION_TIMES)

        print(f"Mutated")
        for weights in next_population:
            print(weights)

        # get best from generated
        for i in range(0, self.MUTATION_TIMES):
            random.shuffle(self.weights_list)
            next_population = self._get_half_best(next_population)
        assert len(next_population) == self.MAX_INDIVIDUALS

        self.weights_list = next_population

    def _get_half_best(self, weights_list):
        best = []
        for i in range(0, len(weights_list), 2):
            h1 = GenericHeuristic(weights_list[i])
            h2 = GenericHeuristic(weights_list[i + 1])
            winner = test_heuristics(h1, h2)
            if winner == 0:
                best.append(weights_list[i])
            else:
                best.append(weights_list[i + 1])
        return best

    def _mutate_weights(self, weights):
        # todo refactor copy
        new_weights = []
        for w in weights:
            new_weights.append((w[0], w[1]))

        pair_to_mutate = random.randint(0, GenericHeuristic.PARAMETER_LIST_LENGTH - 1)
        new_weights[pair_to_mutate] = random_pair()
        return new_weights

    def _crossover_weights(self, weights1, weights2):
        center = random.randint(1, GenericHeuristic.PARAMETER_LIST_LENGTH - 1)
        new_weights1 = []
        new_weights2 = []

        for i in range(0, center):
            new_weights1.append((weights1[i][0], weights1[i][1]))
            new_weights2.append((weights2[i][0], weights2[i][1]))

        for i in range(center, GenericHeuristic.PARAMETER_LIST_LENGTH):
            new_weights2.append((weights1[i][0], weights1[i][1]))
            new_weights1.append((weights2[i][0], weights2[i][1]))

        assert len(new_weights1) == GenericHeuristic.PARAMETER_LIST_LENGTH
        return new_weights1, new_weights2

    def _init_weights(self):
        ans = []
        while len(ans) < self.MAX_INDIVIDUALS:
            ans.append(random_generic_heuristic_weights())
        return ans


if __name__ == '__main__':
    g = GeneticAlgorithm()
    g.start()