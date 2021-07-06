from random import randint
import matplotlib.pyplot as plt
import time
import GeneticSolve

index = []
for i in range(24):
    index.append((i))
MIN = -10000000
default_data = {
    "capacity": 17000,
    "init_charge": 5000,
    "price_schedule": [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 2, 3, 5, 5, 5, 4.5, 3, 3, 3, 3, 4.5, 5, 7, 9, 11, 12, 8, 4],
    "load_schedule": [450, 300, 270, 320, 330, 345, 420, 560,780, 720, 680, 720, 800, 820, 960, 1100, 1280, 1290, 1420,
                      1600, 1720, 1520, 790, 640],
    "constant_load": 350,
    "target_charge": 5000
}
generation_count = 250000

if __name__ == "__main__":
    start_time = time.time()
    gen = GeneticSolve(default_data, 10)
    result = gen.solve(generation_count)
    print('Максимальный результат= ' + str(result["answer"].result))
    print('Покупка и Продажа ЭЭ' + str(result["answer"].test_schedule))
    print('Изменение максимальной прибыли= ' + str(result["process"][::generation_count // 100]))
    print('Изменение заряда в течении 24 часов у Особи=' + str(result["answer"].charge_changes()))
    # Расписание покупки и прожади
    plt.figure(figsize=(8, 5))
    plt.title("Стратегия по продаже энергии в сеть", fontsize=20)
    plt.xlabel("Час", fontsize=15)
    plt.ylabel("Вт", fontsize=15)
    plt.xticks(index)
    plt.bar(index, result["answer"].test_schedule, color="green")
    ax = plt.gca()
    ax.axhline(color='k')
    plt.show()
    #Изменение Расписания от Мутации
    plt.figure(figsize=(8, 5))
    plt.title("Изменение прибыли", fontsize=20)
    plt.xlabel("Существо", fontsize=15)
    plt.ylabel("Прибыль", fontsize=15)
    plt.plot(result["process"][::generation_count // 100], color="black")
    plt.hlines(result["answer"].result, 0, len(result["process"][::generation_count // 100]), color="red")
    plt.grid()
    plt.show()
    # Изменение заряда ЭЭ лучше Особи
    plt.figure(figsize=(8, 5))
    plt.title("Заряд батареи по часам", fontsize=20)
    plt.xlabel("Час", fontsize=15)
    plt.ylabel("Вт/ч", fontsize=15)
    plt.xticks(index)
    plt.plot(index, result["answer"].charge_changes(), color="red", linewidth=4)
    plt.scatter(index, result["answer"].charge_changes(), color="orange", s=100)
    plt.show()
    print("--- %s seconds ---" % (time.time() - start_time))
