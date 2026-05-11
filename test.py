from flask import Flask, render_template, request, jsonify
import numpy as np
import random
import requests as req

app = Flask(__name__)

# ==================================
# DISTANCE
# ==================================

def euclidean_distance(p1, p2):

    return (
        (
            (p1[0] - p2[0]) ** 2
            +
            (p1[1] - p2[1]) ** 2
        ) ** 0.5
    ) * 111000


def get_osrm_distance(p1, p2):

    url = (
        f"https://router.project-osrm.org/"
        f"route/v1/driving/"
        f"{p1[1]},{p1[0]};"
        f"{p2[1]},{p2[0]}"
        f"?overview=false"
    )

    try:

        res = req.get(
            url,
            timeout=3
        )

        if res.status_code != 200:

            return euclidean_distance(
                p1,
                p2
            )

        data = res.json()

        if (
            data.get("routes")
            and
            len(data["routes"]) > 0
        ):

            return data[
                "routes"
            ][0][
                "distance"
            ]

    except Exception as e:

        print(
            "OSRM ERROR:",
            e
        )

    return euclidean_distance(
        p1,
        p2
    )


def build_distance_matrix(points):

    n = len(points)

    matrix = [
        [0.0] * n
        for _ in range(n)
    ]

    print(
        f"\nBuilding matrix ({n} points)"
    )

    for i in range(n):

        for j in range(
            i + 1,
            n
        ):

            print(
                f"Distance "
                f"{i} -> {j}"
            )

            dist = (
                get_osrm_distance(
                    points[i],
                    points[j]
                )
            )

            matrix[i][j] = dist
            matrix[j][i] = dist

    print(
        "Matrix completed"
    )

    return matrix


# ==================================
# GA
# ==================================

def calculate_fitness(
    route,
    dist_matrix
):

    total = 0

    for i in range(
        len(route) - 1
    ):

        total += dist_matrix[
            route[i]
        ][
            route[i + 1]
        ]

    total += dist_matrix[
        route[-1]
    ][
        route[0]
    ]

    return total


def order_crossover(
    p1,
    p2
):

    size = len(p1)

    start, end = sorted(

        random.sample(
            range(size),
            2
        )
    )

    child = [-1] * size

    child[start:end] = (
        p1[start:end]
    )

    pos = end

    for gene in p2:

        if gene not in child:

            while (
                child[
                    pos % size
                ]
                != -1
            ):
                pos += 1

            child[
                pos % size
            ] = gene

    return child


def mutate(route):

    if random.random() < 0.25:

        i, j = random.sample(
            range(len(route)),
            2
        )

        route[i], route[j] = (
            route[j],
            route[i]
        )


# ==================================
# ROUTES
# ==================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


@app.route(
    "/optimize",
    methods=["POST"]
)
def optimize():

    try:

        data = (
            request.get_json()
        )

        points = data.get(
            "points",
            []
        )

        n = len(points)

        if n < 3:

            return jsonify({

                "error":
                "Can it nhat 3 diem"

            }), 400

        print(
            f"\nSTART "
            f"OPTIMIZE "
            f"{n} points"
        )

        # ==================
        # DISTANCE MATRIX
        # ==================

        dist_matrix = (
            build_distance_matrix(
                points
            )
        )

        # ==================
        # GA PARAM
        # ==================

        pop_size = 120
        generations = 150

        population = [

            random.sample(
                range(n),
                n
            )

            for _ in range(
                pop_size
            )
        ]

        best_route = None
        best_distance = (
            float("inf")
        )

        # ==================
        # GA LOOP
        # ==================

        for gen in range(
            generations
        ):

            fitnesses = [

                calculate_fitness(
                    route,
                    dist_matrix
                )

                for route
                in population
            ]

            best_idx = int(
                np.argmin(
                    fitnesses
                )
            )

            if (
                fitnesses[
                    best_idx
                ]
                < best_distance
            ):

                best_distance = (
                    fitnesses[
                        best_idx
                    ]
                )

                best_route = (
                    population[
                        best_idx
                    ][:]
                )

            if gen % 20 == 0:

                print(
                    f"Gen {gen}"
                    f" | "
                    f"Best:"
                    f" {round(best_distance/1000,2)} km"
                )

            new_pop = [
                best_route[:]
            ]

            while (
                len(new_pop)
                < pop_size
            ):

                child = (
                    order_crossover(
                        random.choice(
                            population
                        ),
                        random.choice(
                            population
                        )
                    )
                )

                mutate(child)

                new_pop.append(
                    child
                )

            population = (
                new_pop
            )

        print(
            "FINISHED"
        )

        return jsonify({

            "best_route":
            best_route,

            "best_distance":
            round(
                best_distance,
                2
            )
        })

    except Exception as e:

        print(
            "ERROR:",
            e
        )

        return jsonify({
            "error":
            str(e)
        }), 500


# ==================================
# MAIN
# ==================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5050,
        debug=False,
        use_reloader=False
    )