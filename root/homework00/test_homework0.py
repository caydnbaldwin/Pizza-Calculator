from byu_pytest_utils import max_score, with_import
from haggis.objects import copy_func
from itertools import zip_longest
import builtins

default_constants = {
    "PEOPLE_PER_LARGE": 7,
    "PEOPLE_PER_MEDIUM": 3,
    "PEOPLE_PER_SMALL": 1,
    "DIAMETER_LARGE": 20,
    "DIAMETER_MEDIUM": 16,
    "DIAMETER_SMALL": 12,
    "COST_LARGE": 14.68,
    "COST_MEDIUM": 11.48,
    "COST_SMALL": 7.28,
    "PI": 3.14159265
}


def make_test(inputs, outputs, constants=default_constants):

    def mocked_input_maker(first_input, second_input):
        def generator():
            yield first_input
            yield second_input
            n = 0
            while True:
                n += 1
                yield f"`input` called {n} more times than expected"

        g = generator()

        def mocked_input(*args, **kwargs):
            if len(args) + len(kwargs) > 0:
                print(*args, **kwargs)
            return next(g)

        return mocked_input

    def edit_globals(main_func):
        """Adjust the constants in all functions __globals__"""

        imported_globals = main_func.__globals__
        globals_with_constants = imported_globals | constants

        for func in filter(callable, imported_globals.values()):
            name = func.__name__
            new_func = copy_func(globals_with_constants[name], globals_with_constants, module=__name__)
            globals_with_constants[name] = new_func

        return globals_with_constants["main"]

    numPeople, tipPercent = inputs
    nLarge, nMedium, nSmall, totalArea, indvArea, totalCost = outputs
    @with_import("homework0", "main")
    def test(main, monkeypatch, capsys):
        monkeypatch.setattr(builtins, 'input', mocked_input_maker(numPeople, tipPercent))

        main = edit_globals(main)
        main()

        observed = capsys.readouterr().out
        expected = f"Please enter how many guests to order for:\n{nLarge} large pizzas, {nMedium} medium pizzas, and {nSmall} small pizzas will be needed.\n\nA total of {totalArea} square inches of pizza will be ordered ({indvArea} per guest).\nPlease enter the tip as a percentage (i.e. 10 means 10%):\nThe total cost of the event will be: ${totalCost}.\n\n"

        for expected, observed in zip_longest(expected.split("\n"), observed.split("\n"), fillvalue="Wrong number of lines"):
            assert observed == expected

    return test


@max_score(4)
def test_1_person_35_tip(monkeypatch, capsys):
    make_test([1, 35], ['0', '0', '1', '113.10', '113.10', '9.83'], default_constants)(monkeypatch, capsys)


@max_score(4)
def test_3_person_80_tip(monkeypatch, capsys):
    make_test([3, 80], ['0', '1', '0', '201.06', '67.02', '20.66'], default_constants)(monkeypatch, capsys)


@max_score(4)
def test_7_person_80_tip(monkeypatch, capsys):
    make_test([7, 80], ['1', '0', '0', '314.16', '44.88', '26.42'], default_constants)(monkeypatch, capsys)


@max_score(4)
def test_4_person_35_tip(monkeypatch, capsys):
    make_test([4, 35], ['0', '1', '1', '314.16', '78.54', '25.33'], default_constants)(monkeypatch, capsys)


@max_score(4)
def test_8_person_80_tip(monkeypatch, capsys):
    make_test([8, 80], ['1', '0', '1', '427.26', '53.41', '39.53'], default_constants)(monkeypatch, capsys)


@max_score(4)
def test_10_person_35_tip(monkeypatch, capsys):
    make_test([10, 35], ['1', '1', '0', '515.22', '51.52', '35.32'], default_constants)(monkeypatch, capsys)


@max_score(4)
def test_11_person_10_tip(monkeypatch, capsys):
    make_test([11, 10], ['1', '1', '1', '628.32', '57.12', '36.78'], default_constants)(monkeypatch, capsys)


@max_score(4)
def test_12_person_80_tip(monkeypatch, capsys):
    make_test([12, 80], ['1', '1', '2', '741.42', '61.78', '73.30'], default_constants)(monkeypatch, capsys)


@max_score(4)
def test_13_person_80_tip(monkeypatch, capsys):
    make_test([13, 80], ['1', '2', '0', '716.28', '55.10', '67.75'], default_constants)(monkeypatch, capsys)


@max_score(4)
def test_14_person_10_tip(monkeypatch, capsys):
    make_test([14, 10], ['2', '0', '0', '628.32', '44.88', '32.30'], default_constants)(monkeypatch, capsys)


doubled_constants = {k: v * 2 for k, v in default_constants.items()}


@max_score(2)
def test_15_person_35_tip(monkeypatch, capsys):
    make_test([15, 35], ['1', '0', '1', '3418.05', '227.87', '59.29'], doubled_constants)(monkeypatch, capsys)


@max_score(3)
def test_16_person_80_tip(monkeypatch, capsys):
    make_test([16, 80], ['1', '0', '1', '3418.05', '213.63', '79.06'], doubled_constants)(monkeypatch, capsys)


@max_score(2)
def test_17_person_10_tip(monkeypatch, capsys):
    make_test([17, 10], ['1', '0', '2', '4322.83', '254.28', '64.33'], doubled_constants)(monkeypatch, capsys)


@max_score(3)
def test_100_person_80_tip(monkeypatch, capsys):
    make_test([100, 80], ['7', '0', '1', '18497.70', '184.98', '396.14'], doubled_constants)(monkeypatch, capsys)
