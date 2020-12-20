import random

from heuristics.generic_heuristic import GenericHeuristic
from training import random_generic_heuristic_weights, test_heuristics, random_pair


class GeneticAlgorithm:
    MAX_POPULATIONS = 10000
    MAX_INDIVIDUALS = 40
    # MUTATION_TIMES = 3
    STABILITY_PERCENTAGE = 0.9
    MUTATION_PROBABILITY = 0.027
    CROSSOVER_PROBABILITY = 0.2

    # 0.4 / (l*n) (l - elements of heuristic, n - individuals)
    # crossover with probability
    # in-place

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
    starting = [
        [(15.793412769676774, 1), (8.761758383139512, 1), (-10.91580903389827, 1), (-5.782174161944071, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(5.307822896065371, 1), (8.761758383139512, 1), (-10.91580903389827, 1), (-4.361817717868257, 1),
         (0.4332294370422939, 1), (1.78721893193003, 1)],
        [(15.793412769676774, 1), (8.761758383139512, 1), (-10.91580903389827, 1), (-4.361817717868257, 1),
         (0.4332294370422939, 1), (1.78721893193003, 1)],
        [(17.22148311388888, 1), (3.7476966854700264, 1), (-10.91580903389827, 1), (-5.667497098337936, 1),
         (-0.21928301421064533, 1), (1.78721893193003, 1)],
        [(18.401053391178237, 1), (3.7476966854700264, 1), (-6.299253436616747, 1), (-4.361817717868257, 1),
         (0.4332294370422939, 1), (-3.608443822449125, 1)],
        [(18.105259307542788, 1), (3.7476966854700264, 1), (-10.91580903389827, 1), (-4.361817717868257, 1),
         (0.4332294370422939, 1), (-4.322653838849488, 1)],
        [(15.793412769676774, 1), (8.761758383139512, 1), (-10.91580903389827, 1), (-4.361817717868257, 1),
         (0.4332294370422939, 1), (-4.989838674899376, 1)],
        [(18.401053391178237, 1), (3.7476966854700264, 1), (-8.79114233818268, 1), (-0.5616020274539442, 1),
         (0.4332294370422939, 1), (1.78721893193003, 1)],
        [(15.793412769676774, 1), (8.761758383139512, 1), (-10.91580903389827, 1), (-4.361817717868257, 1),
         (0.4332294370422939, 1), (1.78721893193003, 1)],
        [(15.793412769676774, 1), (8.761758383139512, 1), (-10.91580903389827, 1), (-4.361817717868257, 1),
         (0.4332294370422939, 1), (1.78721893193003, 1)],
        [(17.22148311388888, 1), (7.937580998873643, 1), (-10.91580903389827, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(9.641645271262528, 1), (3.7476966854700264, 1), (-10.91580903389827, 1), (-5.667497098337936, 1),
         (-0.21928301421064533, 1), (1.78721893193003, 1)],
        [(18.401053391178237, 1), (8.761758383139512, 1), (-10.91580903389827, 1), (-4.361817717868257, 1),
         (1.4732076829875351, 1), (1.78721893193003, 1)],
        [(15.793412769676774, 1), (3.7476966854700264, 1), (-10.91580903389827, 1), (-4.361817717868257, 1),
         (0.4332294370422939, 1), (-4.322653838849488, 1)],
        [(9.641645271262528, 1), (7.937580998873643, 1), (-10.91580903389827, 1), (-0.6177065329265181, 1),
         (-1.4816960386162217, 1), (4.2556740961157145, 1)],
        [(15.793412769676774, 1), (8.761758383139512, 1), (-10.91580903389827, 1), (-7.203982664712683, 1),
         (0.4332294370422939, 1), (1.78721893193003, 1)],
        [(9.641645271262528, 1), (7.937580998873643, 1), (-2.640449260249926, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(9.641645271262528, 1), (1.9401111789825372, 1), (-2.640449260249926, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(18.401053391178237, 1), (3.7476966854700264, 1), (-10.91580903389827, 1), (-4.361817717868257, 1),
         (0.4332294370422939, 1), (1.6677103631997499, 1)],
        [(15.793412769676774, 1), (8.761758383139512, 1), (-10.91580903389827, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(9.641645271262528, 1), (7.937580998873643, 1), (-10.91580903389827, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(1.7172589212162421, 1), (1.418487477114705, 1), (-10.91580903389827, 1), (-10.659785293290518, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(9.641645271262528, 1), (7.937580998873643, 1), (-10.91580903389827, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(4.72830720683494, 1), (3.7476966854700264, 1), (-10.91580903389827, 1), (-1.0400333558279096, 1),
         (0.4332294370422939, 1), (6.3159155367397135, 1)],
        [(17.22148311388888, 1), (3.7476966854700264, 1), (-11.036777010726562, 1), (-5.667497098337936, 1),
         (-0.21928301421064533, 1), (1.78721893193003, 1)],
        [(9.641645271262528, 1), (3.7476966854700264, 1), (-10.91580903389827, 1), (-6.482072150025995, 1),
         (0.4332294370422939, 1), (1.78721893193003, 1)],
        [(15.793412769676774, 1), (8.761758383139512, 1), (-2.3876083899233445, 1), (-9.891316205429362, 1),
         (1.9515319869213437, 1), (1.78721893193003, 1)],
        [(9.641645271262528, 1), (7.937580998873643, 1), (-9.531700732189357, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(9.641645271262528, 1), (3.0121623687714747, 1), (-10.91580903389827, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(15.793412769676774, 1), (8.761758383139512, 1), (-10.91580903389827, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(15.793412769676774, 1), (8.761758383139512, 1), (-10.91580903389827, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (3.884019681190945, 1)],
        [(9.641645271262528, 1), (8.01176824400004, 1), (-2.640449260249926, 1), (-5.667497098337936, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(9.641645271262528, 1), (7.937580998873643, 1), (-2.3876083899233445, 1), (-9.891316205429362, 1),
         (1.9515319869213437, 1), (1.78721893193003, 1)],
        [(18.401053391178237, 1), (7.937580998873643, 1), (-10.91580903389827, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(17.22148311388888, 1), (3.7476966854700264, 1), (-10.91580903389827, 1), (-5.667497098337936, 1),
         (-0.21928301421064533, 1), (-3.608443822449125, 1)],
        [(18.105259307542788, 1), (3.7476966854700264, 1), (-6.299253436616747, 1), (-4.361817717868257, 1),
         (0.4332294370422939, 1), (1.78721893193003, 1)],
        [(15.793412769676774, 1), (7.937580998873643, 1), (-2.640449260249926, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(9.641645271262528, 1), (8.761758383139512, 1), (-10.91580903389827, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(18.105259307542788, 1), (3.7476966854700264, 1), (-7.252160504097515, 1), (-8.305769224686562, 1),
         (-1.4816960386162217, 1), (1.78721893193003, 1)],
        [(9.641645271262528, 1), (7.937580998873643, 1), (-6.299253436616747, 1), (-4.361817717868257, 1),
         (0.4332294370422939, 1), (-3.608443822449125, 1)]

    ]
    g = GeneticAlgorithm(full=starting)
    g.start()
