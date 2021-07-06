class GeneticSolve:
    def __init__(self, data: dict, instance_count):
        self.instances = []
        self.data = data

        for i in range(instance_count):
            self.instances.append(self.Instance(data))
    def hybrid(self, instance_1, instance_2):
        result = self.Instance(self.data, instance_1.test_schedule.copy())
        for hour in range(24):
            if randint(1, 2) == 1:
                result.test_schedule[hour] = instance_2.test_schedule[hour]
        return result
    def solve(self, generation_count=100, start_schedule=None):
        result = {"answer": None, "process": []}
        for instance in self.instances:
            instance.init_correct(start_schedule)
            instance.test()
        for g in range(generation_count):
            count = len(self.instances)
            half = count // 2
            for i in range(half + 1, count):
                index1, index2 = randint(0, half + 1), randint(0, half + 1)
                parent1, parent2 = self.instances[index1], self.instances[index2]
                self.instances[i] = self.hybrid(parent1, parent2)
                self.instances[i].mutate()
            for instance in self.instances:
                instance.test()
            self.instances.sort(key=lambda x: -x.result)
            best = self.instances[0]
            if g % 1000 == 0:
                print(f"{int(g / generation_count * 100)}%: {best.result}")
            result["process"].append(best.result)
            result["answer"] = best
        return result

    class Instance:
        def __init__(self, data, test_schedule=None):
            # capacity
            # init_charge
            # price_schedule
            # load_schedule
            # constant_load
            # target_charge

            self.data = data

            if test_schedule:
                self.test_schedule = test_schedule
            else:
                self.test_schedule = [0] * 24

            self.result = MIN
        def init_correct(self, start_schedule):
            if start_schedule:
                self.test_schedule = start_schedule.copy()
                return

            charge = self.data["init_charge"]

            for hour in range(24):
                load = self.data["constant_load"] + self.data["load_schedule"][hour]

                charge -= load
                self.test_schedule[hour] = -min(4000, (self.data["capacity"] - charge))
                charge -= self.test_schedule[hour]
        def test(self):
            self.result = 0
            charge = self.data["init_charge"]

            for hour in range(24):
                load = self.data["constant_load"] + self.data["load_schedule"][hour]
                trade = self.test_schedule[hour]
                cost = self.data["price_schedule"][hour]

                if load > charge:
                    self.result = MIN
                    return
                charge -= load

                if trade > charge:
                    self.result = MIN
                    return
                charge -= trade
                self.result += trade * cost
                charge = min(charge, self.data["capacity"])

            if charge <= self.data["target_charge"]:
                self.result = MIN
        def charge_changes(self):
            result = []
            charge = self.data["init_charge"]
            for hour in range(24):
                charge = min(self.data["capacity"], charge - self.test_schedule[hour])
                result.append(charge)

            return result
        def mutate(self):
            for mutation in range(randint(1, 10)):
                hour = randint(0, 23)
                trade_type = [-1, 1, 0][randint(0, 2)]
                trade = randint(1000, 4000) * trade_type

                self.test_schedule[hour] = trade
