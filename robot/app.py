from flask import Flask, render_template, request, jsonify
import random
import math

app = Flask(__name__)


def tinh_khoang_cach(p1, p2):

    lat1, lon1 = p1
    lat2, lon2 = p2

    return math.sqrt(
        (lat1 - lat2) ** 2 +
        (lon1 - lon2) ** 2
    ) * 111000


def tao_ma_tran(points):

    n = len(points)

    matrix = [
        [0] * n
        for _ in range(n)
    ]

    for i in range(n):

        for j in range(i + 1, n):

            d = tinh_khoang_cach(
                points[i],
                points[j]
            )

            matrix[i][j] = d
            matrix[j][i] = d

    return matrix



def fitness(route, matrix):

    tong = 0

    for i in range(
        len(route) - 1
    ):

        tong += matrix[
            route[i]
        ][
            route[i + 1]
        ]

    tong += matrix[
        route[-1]
    ][
        route[0]
    ]

    return tong


def crossover(
    parent1,
    parent2
):

    size = len(parent1)

    start, end = sorted(
        random.sample(
            range(size),
            2
        )
    )

    child = [-1] * size

    child[start:end] = (
        parent1[start:end]
    )

    pointer = 0

    for gene in parent2:

        if gene not in child:

            while (
                child[pointer]
                != -1
            ):
                pointer += 1

            child[pointer] = gene

    return child


def mutate(route):

    if random.random() < 0.2:

        i, j = random.sample(
            range(len(route)),
            2
        )

        route[i], route[j] = (
            route[j],
            route[i]
        )


def select(
    population,
    fitnesses
):

    k = min(
        5,
        len(population)
    )

    selected = random.sample(

        list(
            zip(
                population,
                fitnesses
            )
        ),

        k
    )

    selected.sort(
        key=lambda x: x[1]
    )

    return selected[0][0]


@app.route("/")
def home():

    return render_template(
        "index.html"
    )


@app.route(
    "/optimize",
    methods=["POST"]
)
def optimize():

    try:

        data = request.get_json()

        points = data.get(
            "points",
            []
        )

        if len(points) < 3:

            return jsonify({
                "error":
                "Can it nhat 3 diem"
            })

        n = len(points)

        matrix = (
            tao_ma_tran(
                points
            )
        )

        POP_SIZE = 100
        GENERATIONS = 200
        ELITE_SIZE = 5

        population = [

            random.sample(
                range(n),
                n
            )

            for _ in range(
                POP_SIZE
            )
        ]

        best_route = None

        best_distance = float(
            "inf"
        )

        for _ in range(
            GENERATIONS
        ):

            fitnesses = [

                fitness(
                    route,
                    matrix
                )

                for route
                in population
            ]

            ranked = sorted(

                zip(
                    population,
                    fitnesses
                ),

                key=lambda x: x[1]
            )

            if (
                ranked[0][1]
                < best_distance
            ):

                best_distance = (
                    ranked[0][1]
                )

                best_route = (
                    ranked[0][0][:]
                )

            new_population = [

                ranked[i][0][:]

                for i in range(
                    ELITE_SIZE
                )
            ]

            while (
                len(new_population)
                < POP_SIZE
            ):

                p1 = select(
                    population,
                    fitnesses
                )

                p2 = select(
                    population,
                    fitnesses
                )

                child = crossover(
                    p1,
                    p2
                )

                mutate(child)

                new_population.append(
                    child
                )

            population = (
                new_population
            )

        route_distances = []

        if best_route is not None:

            for i in range(len(best_route)):

                a = best_route[i]
                b = best_route[(i + 1) % len(best_route)]

                route_distances.append(
                    round(matrix[a][b], 2)
                )

        return jsonify({
            "best_route": best_route,
            "best_distance": round(best_distance, 2),
            "points_count": n,
            "route_distances": route_distances
        })

    except Exception as e:

        return jsonify({
            "error":
            str(e)
        })


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5050,
        debug=True,
        use_reloader=False
    )