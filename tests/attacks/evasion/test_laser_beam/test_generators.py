# MIT License
#
# Copyright (C) The Adversarial Robustness Toolbox (ART) Authors 2021
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import numpy as np
import pytest
from art.attacks.evasion.laser_attack.utils import ImageGenerator

from fixtures import image_shape, laser_generator, max_laser_beam, min_laser_beam


@pytest.mark.parametrize("execution_number", range(100))
def test_if_random_laser_beam_is_in_ranges(laser_generator, min_laser_beam, max_laser_beam, execution_number):
    random_laser = laser_generator.random()
    np.testing.assert_array_less(random_laser.to_numpy(), max_laser_beam.to_numpy())
    np.testing.assert_array_less(min_laser_beam.to_numpy(), random_laser.to_numpy())


@pytest.mark.parametrize("execution_number", range(5))
def test_laser_beam_update(laser_generator, min_laser_beam, max_laser_beam, execution_number):
    random_laser = laser_generator.random()

    arr1 = random_laser.to_numpy()
    arr2 = laser_generator.update_params(random_laser).to_numpy()
    np.testing.assert_array_compare(lambda x, y: not np.allclose(x, y), arr1, arr2)
    np.testing.assert_array_less(arr2, max_laser_beam.to_numpy())
    np.testing.assert_array_less(min_laser_beam.to_numpy(), arr2)


@pytest.mark.parametrize("execution_number", range(5))
def test_image_generator(laser_generator, image_shape, execution_number):
    img_gen = ImageGenerator()
    laser = laser_generator.random()
    arr1 = img_gen.generate_image(laser, image_shape)
    np.testing.assert_array_compare(lambda x, y: not np.allclose(x, y), arr1, np.zeros(image_shape))
