# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""General utilities"""
import importlib
from enum import Enum

import numpy
import torch

from pytorch_lightning.utilities.apply_func import move_data_to_device
from pytorch_lightning.utilities.distributed import rank_zero_info, rank_zero_only, rank_zero_warn
from pytorch_lightning.utilities.parsing import AttributeDict, flatten_dict, is_picklable


def _module_available(module_path: str) -> bool:
    """Testing if given module is avalaible in your env

    >>> _module_available('system')
    True
    >>> _module_available('bla.bla')
    False
    """
    mods = module_path.split('.')
    assert mods, 'nothing given to test'
    # it has to be tested as per partets
    for i in range(1, len(mods)):
        module_path = '.'.join(mods[:i])
        if importlib.util.find_spec(module_path) is None:
            return False
    return True


APEX_AVAILABLE = _module_available("apex.amp")
NATIVE_AMP_AVALAIBLE = hasattr(torch.cuda, "amp") and hasattr(torch.cuda.amp, "autocast")

FLOAT16_EPSILON = numpy.finfo(numpy.float16).eps
FLOAT32_EPSILON = numpy.finfo(numpy.float32).eps
FLOAT64_EPSILON = numpy.finfo(numpy.float64).eps


class AMPType(Enum):
    APEX = 'apex'
    NATIVE = 'native'
