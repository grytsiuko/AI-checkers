import random

from heuristics.generic_heuristic import GenericHeuristic
from training import random_generic_heuristic_weights, test_heuristics, random_pair


class GeneticAlgorithm:
    MAX_POPULATIONS = 10000
    MAX_INDIVIDUALS = 16
    MUTATION_TIMES = 2

    def __init__(self, init_weights=None):
        assert self.MAX_INDIVIDUALS % 4 == 0
        self.weights_list = self._init_weights(init_weights)
        self.current_population = 0
        self._file = None

    def start(self):
        while self.current_population < self.MAX_POPULATIONS:
            self._run_population()
            self.current_population = self.current_population + 1
        self._file = open('genetic_statistics.txt', 'a')
        self._write_statistics("\n\n\n### RESULT ###", self.weights_list, True)
        self._file.close()

    def _run_population(self):
        self._file = open('genetic_statistics.txt', 'a')
        self._write_statistics(f"### POPULATION {self.current_population} ###", self.weights_list, True)

        # # get survivals
        # random.shuffle(self.weights_list)
        # survived_list = self._get_half_best(self.weights_list)
        # assert len(survived_list) == self.MAX_INDIVIDUALS // 2
        #
        # self._write_statistics(f"Survived", survived_list)

        # get leader
        leaders = self.weights_list
        while len(leaders) > 1:
            random.shuffle(leaders)
            leaders = self._get_half_best(leaders)
        assert len(leaders) == 1

        self._write_statistics(f"Leader", leaders, True)

        # init next population
        next_population = []

        # crossover
        random.shuffle(self.weights_list)
        for i in range(0, self.MAX_INDIVIDUALS, 2):
            weights1 = self.weights_list[i]
            weights2 = self.weights_list[i + 1]
            new_weights1, new_weights2 = self._crossover_weights(weights1, weights2)
            next_population += [weights1, weights2, new_weights1, new_weights2]
        assert len(next_population) == self.MAX_INDIVIDUALS * 2

        self._write_statistics(f"Crossed", next_population)

        # mutations
        for i in range(0, self.MAX_INDIVIDUALS * 2):
            curr = next_population[i]
            for k in range(0, (2 ** self.MUTATION_TIMES) - 1):
                next_population.append(self._mutate_weights(curr))
        assert len(next_population) == self.MAX_INDIVIDUALS * 2 * (2 ** self.MUTATION_TIMES)

        self._write_statistics(f"Mutated", next_population)

        # get best from generated
        for i in range(0, self.MUTATION_TIMES + 1):
            random.shuffle(self.weights_list)
            next_population = self._get_half_best(next_population)
        assert len(next_population) == self.MAX_INDIVIDUALS

        self.weights_list = next_population
        self._file.close()

    def _write_statistics(self, title, weights, console=False):
        if console:
            print(title)
            for weight in weights:
                print(weight)
            print()
        self._file.write(title + '\n')
        for weight in weights:
            self._file.write(str(weight) + '\n')
        self._file.write('\n' + '\n')

    def _get_half_best(self, weights_list):
        best = []
        for i in range(0, len(weights_list), 2):
            h1 = GenericHeuristic(weights_list[i])
            if i + 1 == len(weights_list):
                best.append(weights_list[i])
                break
            h2 = GenericHeuristic(weights_list[i + 1])
            diff = test_heuristics(h1, h2)
            if diff > 0:
                best.append(weights_list[i])
            else:
                best.append(weights_list[i + 1])
        return best

    def _mutate_weights(self, weights):
        # todo refactor copy
        new_weights = []
        for w in weights:
            new_weights.append((w[0], w[1]))

        index_pair_to_mutate = random.randint(0, GenericHeuristic.PARAMETER_LIST_LENGTH - 1)
        id_to_change = random.randint(0, 2)

        old_tuple = new_weights[index_pair_to_mutate]

        new_element1 = old_tuple[0]
        new_element2 = old_tuple[1]

        if id_to_change == 0:  # sign
            new_element1 *= -1
        if id_to_change == 1:  # abs
            new_element1 = random.uniform(0, GenericHeuristic.MAX_COEF) \
                           * (1 if new_element1 > 0 else -1)
        if id_to_change == 2:  # pow
            new_element2 = random.randint(GenericHeuristic.MIN_POW, GenericHeuristic.MAX_POW)

        new_weights[index_pair_to_mutate] = (new_element1, new_element2)
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

    def _init_weights(self, init_weights):
        ans = [init_weights]
        if init_weights is None:
            while len(ans) < self.MAX_INDIVIDUALS:
                ans.append(random_generic_heuristic_weights())
        else:
            while len(ans) < self.MAX_INDIVIDUALS:
                ans.append(self._mutate_weights(init_weights))
        return ans


if __name__ == '__main__':
    g = GeneticAlgorithm([(5,1), (10,1), (-5, 1), (-10, 1)])
    g.start()
