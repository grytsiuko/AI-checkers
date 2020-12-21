import random

from heuristics.generic_heuristic import GenericHeuristic
from training import random_generic_heuristic_weights, test_heuristics, random_pair


class GeneticAlgorithm:
    MAX_POPULATIONS = 10000
    MAX_INDIVIDUALS = 32
    STABILITY_PERCENTAGE = 0.99
    MUTATION_PROBABILITY = 0.01
    CROSSOVER_PROBABILITY = 0.05

    def __init__(self, init_weights=None, full=None):
        assert self.MAX_INDIVIDUALS % 4 == 0
        if full is not None:
            self.weights_list = full
        else:
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

        # get survivals
        random.shuffle(self.weights_list)
        best = self._get_half_best(self.weights_list)
        assert len(best) == self.MAX_INDIVIDUALS // 2

        self._write_statistics(f"Best", best)

        # get leader
        if self.current_population % 10 == 0 and self.current_population > 0:
            leaders = best
            while len(leaders) > 1:
                random.shuffle(leaders)
                leaders = self._get_half_best(leaders)
            assert len(leaders) == 1

            self._write_statistics(f"Leader", leaders, True)

        # init next population
        ancestors = self._populate_list_random(best, self.MAX_INDIVIDUALS)
        assert len(ancestors) == self.MAX_INDIVIDUALS

        # crossover
        random.shuffle(ancestors)
        after_crossover = []
        for i in range(0, self.MAX_INDIVIDUALS, 2):
            weights1 = ancestors[i]
            weights2 = ancestors[i + 1]
            new_weights1, new_weights2 = self._crossover_weights(weights1, weights2)
            after_crossover += [new_weights1, new_weights2]
        assert len(after_crossover) == self.MAX_INDIVIDUALS

        self._write_statistics(f"Crossed", after_crossover)

        # mutations
        after_mutations = []
        for i in range(0, self.MAX_INDIVIDUALS):
            to_mutate = after_crossover[i]
            after_mutations.append(self._mutate_weights(to_mutate))
        assert len(after_mutations) == self.MAX_INDIVIDUALS

        self._write_statistics(f"Mutated", after_mutations)

        self.weights_list = after_mutations
        self._file.close()

    def _populate_list_random(self, weights_list, amount):
        ans = []
        length = len(weights_list)
        for i in range(0, amount):
            index = random.randint(0, length - 1)
            ans.append(self._copy_list(weights_list[index]))
        return ans

    def _copy_list(self, weights):
        new_weights = []
        for w in weights:
            new_weights.append((w[0], w[1]))
        return new_weights

    def _write_statistics(self, title, weights, console=False):
        if console:
            print(title)
            for weight in weights:
                print(weight, ',')
            print()
        self._file.write(title + '\n')
        for weight in weights:
            self._file.write(str(weight) + ',\n')
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
        new_weights = []
        for w in weights:
            new0 = w[0]
            new1 = w[1]
            if random.random() < self.MUTATION_PROBABILITY:
                new0 = new0 * self.STABILITY_PERCENTAGE \
                       + random.uniform(GenericHeuristic.MIN_COEF, GenericHeuristic.MAX_COEF) * (
                               1 - self.STABILITY_PERCENTAGE)

            new_weights.append((new0, new1))
        return new_weights

    def _crossover_weights(self, weights1, weights2):
        if random.random() < (1 - self.CROSSOVER_PROBABILITY):
            return weights1, weights2

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
        ans = []
        if init_weights is None:
            while len(ans) < self.MAX_INDIVIDUALS:
                ans.append(random_generic_heuristic_weights())
        else:
            ans.append(init_weights)
            while len(ans) < self.MAX_INDIVIDUALS:
                ans.append(self._mutate_weights(init_weights))
        return ans


if __name__ == '__main__':
    starting = None
    g = GeneticAlgorithm([(12.127784701926773, 1), (14.440556624041355, 1), (-8.02422920639554, 1), (-5.630438776072073, 1), (0, 1), (-0.18818505411897024, 1), (0.44122390158843006, 1), (-0.1228863582111075, 1)])
    g.start()
