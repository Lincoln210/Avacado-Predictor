# SYSTEM IMPORTS
from collections import defaultdict
from typing import Dict, List, Tuple, Type
import os
import sys
from pprint import pprint


_cd_: str = os.path.abspath(os.path.dirname(__file__))
for _dir_ in [_cd_]:
    if _dir_ not in sys.path:
        sys.path.append(_dir_)
del _cd_


# PYTHON PROJECT IMPORTS
from data import Color, Softness, GoodToEat, load_data



# TYPES DEFINED IN THIS MODULE
AvacadoPredictorType: Type = Type["AvacadoPredictor"]


class AvacadoPredictor(object):
    def __init__(self: AvacadoPredictorType) -> None:
        self.color_given_good_to_eat_pmf: Dict[GoodToEat, Dict[Color, float]] = defaultdict(lambda: defaultdict(float))
        self.softness_given_good_to_eat_pmf: Dict[GoodToEat, Dict[Softness, float]] = defaultdict(lambda: defaultdict(float))
        self.good_to_eat_prior: Dict[GoodToEat, float] = defaultdict(float)


    def fit(self: AvacadoPredictorType,
            data: List[Tuple[Color, Softness, GoodToEat]]
            ) -> AvacadoPredictorType:
        total_avacados = len(data)
        for color, softness, good_to_eat in data:
            self.good_to_eat_prior[good_to_eat] += 1
            self.color_given_good_to_eat_pmf[good_to_eat][color] += 1
            self.softness_given_good_to_eat_pmf[good_to_eat][softness] += 1

        for good_to_eat in self.good_to_eat_prior:
            self.good_to_eat_prior[good_to_eat] = self.good_to_eat_prior[good_to_eat] / total_avacados

        for good_to_eat in self.color_given_good_to_eat_pmf:
            total_counts: int = sum(self.color_given_good_to_eat_pmf[good_to_eat].values())
            for color in self.color_given_good_to_eat_pmf[good_to_eat]:
                self.color_given_good_to_eat_pmf[good_to_eat][color] /= total_counts

        for good_to_eat in self.softness_given_good_to_eat_pmf:
            total_counts: int = sum(self.softness_given_good_to_eat_pmf[good_to_eat].values())
            for softness in self.softness_given_good_to_eat_pmf[good_to_eat]:
                self.softness_given_good_to_eat_pmf[good_to_eat][softness] /= total_counts

        return self


    def predict_color_proba(self: AvacadoPredictorType,
                            X: List[Color]
                            ) -> List[List[Tuple[GoodToEat, float]]]:
        probs_per_example: List[List[Tuple[GoodToEat, float]]] = list()
        
    def predict_softness_proba(self: AvacadoPredictorType,
                               X: List[Softness]
                               ) -> List[List[Tuple[GoodToEat, float]]]:
        probs_per_example: List[List[Tuple[GoodToEat, float]]] = list()
    
    # EXTRA CREDIT
    def predict_color(self: AvacadoPredictorType,
                    X: List[Color]
                    ) -> List[GoodToEat]:

    def predict_softness(self: AvacadoPredictorType,
                    X: List[Color]
                    ) -> List[GoodToEat]:




def accuracy(predictions: List[GoodToEat],
             actual: List[GoodToEat]
             ) -> float:
    if len(predictions) != len(actual):
        raise ValueError(f"ERROR: expected predictions and actual to be same length but got pred={len(predictions)}" +
            " and actual={len(actual)}")

    num_correct: float = 0
    for pred, act in zip(predictions, actual):
        num_correct += int(pred == act)

    return num_correct / len(predictions)


def main() -> None:
    data: List[Tuple[Color, Softness, GoodToEat]] = load_data()

    color_data: List[Color] = [color for color, _, _ in data]
    softness_data: List[Softness] = [softness for _, softness, _ in data]
    good_to_eat_data: List[GoodToEat] = [good_to_eat for _, _, good_to_eat in data]

    m: AvacadoPredictor = AvacadoPredictor().fit(data)

    print("good to eat prior")
    pprint(m.good_to_eat_prior)
    print()
    print()

    print("color given good to eat pmf")
    pprint(m.color_given_good_to_eat_pmf)
    print()
    print()

    print("softness given good to eat pmf")
    pprint(m.softness_given_good_to_eat_pmf)

    # if you do the extra credit be sure to uncomment these lines!
    print("accuracy when predicting only on color: ", accuracy(m.predict_color(color_data), good_to_eat_data))

    print("accuracy when predicting only on softness: ", accuracy(m.predict_softness(softness_data), good_to_eat_data))


if __name__ == "__main__":
    main()

