#############
##  Setup  ##
#############


import kdtree  # pip install kdtree

from random import randint, choices, seed
from collections import namedtuple
from typing import Tuple, List

# giant list of (some) pantone names
from pantones import pantones

# timing
import timeit
import functools

# random seed
seed(333)

# simplified tuple
RGB = namedtuple("RGB", ["r", "g", "b"])
FOURD = namedtuple("FOURD", ["d1", "d2", "d3", "d4"])

# novelty colour names for generating dataset
generate_colours = "sepia,buttermilk,marmalade,grey,mahogany,indigo,periwinkle,orchid,cerulean,emerald".split(
    ","
)
generate_animals = "African Palm Civet,Humpback Whale,Common Buzzard,Glow Worm,Cinereous Vulture,Emperor Tamarin,Kodiak Bear,Tapanuli Orangutan, Emperor Gum Moth".split(
    ","
)

# real colour names
# pantones = [] # pulled to own file

# map of rgb:name
# prgb_map = {rgb_from_hex(k): v for (k, v) in zip(rgb, pantones)} #unused

# total size of rgb space is 1,6581,375
# num elements used for benchmark = 1000 |10,000 | 100,000 |1,000,000

########################
##  Helper Functions  ##
########################


def rgb_from_hex(hexval: str) -> Tuple[int, int, int]:
    rgb = tuple(int(hexval[i : i + 2], 16) for i in (0, 2, 4))
    return RGB(rgb[0], rgb[1], rgb[2])


def generate_pantone() -> Tuple[str, Tuple[int, int, int]]:
    colour = choices(generate_colours, k=1)
    animal = choices(generate_animals, k=1)
    name = f"{animal[0]} {colour[0]}"

    r, g, b = randint(0, 255), randint(0, 255), randint(0, 255)
    return (f"{name}", RGB(r, g, b))


def generate_4d() -> Tuple[int, int, int, int]:
    d1, d2, d3, d4 = randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)
    return (f"name", FOURD(d1, d2, d3, d4))


# unused -> kdtree has sort method equivalent to below on creation
def sort_rgb_list(rgb_list: List[Tuple]) -> List[Tuple]:
    s = sorted(rgb_list, key=lambda t: (t[0], t[1], t[2]))
    return s


# unused -> kdtree has sort method equivalent to below on creation
def sort_4d_list(_4dlist: List[Tuple]) -> List[Tuple]:
    s = sorted(_4dlist, key=lambda t: (t[0], t[1], t[2], [t3]))
    return s


# helper function for seeded_tree
def seed_set(dataset: List[RGB], percent=10):  # -> seed:List[RGB],_set:List[RGB]
    """ helper """
    _set = dataset
    set_len = len(dataset)

    n = set_len // percent  # 10% as seed
    seed = _set[:n]
    _set = _set[n:]

    return seed, _set


# helper function for time_searches()
def search_timer(tree, point, dist):
    t = timeit.repeat(
        functools.partial(tree.search_nn_dist, point, dist ** 2), repeat=rpt, number=num
    )
    return t


##############################################
##      Tree construction + timings         ##
##############################################


# creates a presorted tree
def presorted_tree(dataset: List[RGB]) -> kdtree:
    tree = kdtree.create(point_list=dataset)
    return tree


# creates a random tree
def random_tree(dataset: List[RGB]) -> kdtree:
    tree = kdtree.create(dimensions=len(dataset[0]))

    if dataset:
        for rgb in dataset:
            tree.add(rgb)
    return tree


# creates a seeded tree
def seeded_tree(seed: List[RGB], dataset: List[RGB]) -> kdtree:
    if seed:
        tree = kdtree.create(point_list=seed)

        if dataset:
            for rgb in dataset:
                tree.add(rgb)
        return tree
    return None  # should not reach


# times construction of trees given datasets
def time_constructions(rpt: int, num: int, datasets):

    construction_times = {"pre": [], "random": [], "seeded": []}

    for i in range(len(datasets)):
        _set = datasets[i]
        set_len = len(_set)

        t = timeit.repeat(
            functools.partial(presorted_tree, _set), repeat=rpt, number=num
        )
        construction_times["pre"].append([set_len, t])

        t = timeit.repeat(functools.partial(random_tree, _set), repeat=rpt, number=num)
        construction_times["random"].append([set_len, t])

        # _set = _set[n:]
        seed, _set = seed_set(_set)

        t = timeit.repeat(
            functools.partial(seeded_tree, seed, _set), repeat=rpt, number=num
        )
        construction_times["seeded"].append([set_len, t])

    return construction_times


# creates trees for search timing
def create_trees(data_set):

    pre_trees = [[len(data), presorted_tree(data)] for data in data_set]
    random_trees = [[len(data), random_tree(data)] for data in data_set]
    seed_sets = [(seed_set(data)) for data in data_set]
    seed_trees = [
        [len(data_set[i]), seeded_tree(seed_sets[i][0], seed_sets[i][1])]
        for i in range(len(seed_sets))
    ]

    return pre_trees, seed_trees, random_trees


# performs searches at distances for point in pre,seed,random trees
def time_searches(
    rpt: int, num: int, pre_trees, seed_trees, random_trees, point, distances
):

    search_times = {"pre": [], "random": [], "seeded": []}

    for dist in distances:
        for i in range(len(pre_trees)):

            # pre
            trees = pre_trees
            n_elem = trees[i][0]
            tree = trees[i][1]

            search_times["pre"].append([n_elem, dist, search_timer(tree, point, dist)])

            # random
            trees = random_trees

            n_elem = trees[i][0]
            tree = trees[i][1]
            search_times["random"].append(
                [n_elem, dist, search_timer(tree, point, dist)]
            )

            # seeded
            trees = seed_trees

            n_elem = trees[i][0]
            tree = trees[i][1]
            search_times["seeded"].append(
                [n_elem, dist, search_timer(tree, point, dist)]
            )

    return search_times


#################################################
##      Generation + Execution Timing  3D      ##
#################################################


# generate sets for insertion to kd-tree at 10^3,10^4,10^5 size
pantone_sets = [
    [generate_pantone()[1] for i in range(1341 * 10 ** j)] for j in range(4)
]

# timeit and dataset paramaters
rpt = 1
num = 1
# set the dataset
dataset = pantone_sets
# search paramaters
point = RGB(123, 123, 123)  # <--set the point to search
distances = [16, 32, 64, 128]  # <--fill the distances

# create trees for search
pre_trees, seed_trees, random_trees = create_trees(dataset)


# time how long it takes to construct kd-trees
construction_times = time_constructions(rpt, num, dataset)

# time how long it takes to search kd-trees
search_times = time_searches(
    rpt, num, pre_trees, seed_trees, random_trees, point, distances
)

######### Results can be written to files ############
# print("construct:")
# for i in construction_times:
#     print(i,construction_times[i])
# print("search:")
# for i in search_times:
#     print(i, search_times[i])
######################################################


#################################################
##      Generation + Execution Timing  4D      ##
#################################################

fourd_sets = [[generate_4d()[1] for i in range(1341 * 10 ** j)] for j in range(4)]

rpt = 1
num = 1
dataset = fourd_sets
point = FOURD(123, 123, 123, 123)
distances = [16, 32, 64, 128]

pre_trees, seed_trees, random_trees = create_trees(dataset)
fconstruction_times = time_constructions(rpt, num, dataset)
fsearch_times = time_searches(
    rpt, num, pre_trees, seed_trees, random_trees, point, distances
)

######### Results can be written to files ############
# print("construct:")
# for i in construction_times:
#     print(i,construction_times[i])
# print("search:")
# for i in search_times:
#     print(i, search_times[i])
######################################################