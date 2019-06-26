from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from mock import patch
import numpy as np

from pyxpb.detectors import MonoDetector

mono = MonoDetector(shape=(2000, 2000), pixel_size=0.2,
                    sample_detector=700, energy=100,
                    delta_energy=0.5)
mono.add_material('Fe')


def test_intensity_profiles():
    phi = np.pi / 3.2
    profile_0 = mono.intensity(phi, background=0, x_axis='q',
                             strain_tensor=(0.2, 0.2, 0.3))
    profile_180 = mono.intensity(phi-np.pi, background=0, x_axis='q',
                               strain_tensor=(0.2, 0.2, 0.3))
    assert np.allclose(profile_0[1]['Fe'], profile_180[1]['Fe'])

    # Test a few combinations of parameters
    mono.intensity(0, background=0, x_axis='2theta',
                   strain_tensor=(0.2, 0.2, 0.3))

    mono.intensity([0, np.pi/7], background=0, x_axis='2theta',
                   strain_tensor=(0., 0., 0.))


def test_equal_quadrants():
    rings = mono.rings(strain_tensor=(0.2, 0.2, 0.3), crop=0.6,
                       exclude_criteria=0.075, background=0)
    # FInd centre for odd/even number of pixels
    split_x = rings.shape[0] // 2, -(-rings.shape[0] // 2)
    split_y = rings.shape[1] // 2, -(-rings.shape[1] // 2)

    top_left = rings[:split_y[0], :split_x[0]]
    top_right = rings[:split_y[0], split_x[1]:]
    bottom_left = rings[split_y[1]:, :split_x[0]]
    bottom_right = rings[split_y[1]:, split_x[1]:]

    error = 'Symmetrically opposite quadrants not equal!'
    assert np.allclose(top_left, np.rot90(bottom_right, 2)), error
    assert np.allclose(top_right, np.rot90(bottom_left, 2)), error

@patch("matplotlib.pyplot.show")
def test_plot_intensity(mock_show):
    mock_show.return_value = None
    mono.define_background([0, 1, 2, 3, 4, 5, 6, 7],
                           [0, 2, 3, 3.5, 3.75, 3.5, 3, 2], k=2)
    mono.plot_intensity()
    mono.intensity_factors('Fe', plot=True)


@patch("matplotlib.pyplot.show")
def test_plot_rings(mock_show):
    mock_show.return_value = None
    mono.plot_rings()


if __name__== '__main__':
    test_equal_quadrants()
    test_intensity_profiles()
