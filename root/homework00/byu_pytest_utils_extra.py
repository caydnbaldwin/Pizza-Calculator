import importlib
import os.path
import runpy
from functools import wraps
from pathlib import Path
import inspect
from typing import Union

import pytest
import sys

def log(s):
    with open("/home/lars/log", 'a') as f:
        # print(s)
        f.write(str(s) + "\n")

def with_import_constant(module_name=None, constant_name=None):
    # Create a decorator
    def decorator(test_function):
        # Import function_name from module_name, then run function
        # with function_name passed in as first arg
        nonlocal constant_name
        nonlocal module_name
        params = inspect.signature(test_function).parameters
        first_param = next((pname for pname, _ in params.items())) if len(params) > 0 else ""

        @wraps(test_function)
        def new_test_function(*args, **kwargs):
            try:
                module = importlib.import_module(module_name)
                const = getattr(module, constant_name)
                if "constants" in kwargs.keys():
                    kwargs["constants"][constant_name] = const
                else:
                    kwargs["constants"] = {constant_name: const}
                return test_function(*args, **kwargs)

            except ModuleNotFoundError as err:
                pytest.fail(
                    f'{type(err).__name__}: {err}\n'
                    f'Unable to load {module_name}.py. '
                    f'Was {module_name}.py submitted?'
                )
            except ImportError as err:
                pytest.fail(
                    f'{type(err).__name__}: {err}\n'
                    f'Unable to load {module_name}.py. '
                    f'Are there errors in the file?'
                )
            except KeyError as err:
                pytest.fail(
                    f'{type(err).__name__}: {err}\n'
                    f'Unable to load {function_name} from {module_name}.py. '
                    f'Is {function_name} defined?'
                )

        # Modify signature to look like test_function but without
        # anything filled by with_import
        sig = inspect.signature(test_function)
        sig._parameters = dict(sig.parameters)
        if len(sig.parameters) > 0:
            del sig._parameters[first_param]
        new_test_function.__signature__ = sig

        return new_test_function

    if callable(module_name):
        # The decorator was used without arguments,
        # so this call is the decorator
        func = module_name
        module_name = None
        return decorator(func)
    else:
        return decorator
