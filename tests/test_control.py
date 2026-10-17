from uuv_mission.control import PDController
import pytest

def test_calculate(): 
    """Test the calculate function of PDController"""
    controller = PDController()
    test_ref = 10
    test_obs = 8
    result = controller.calculate(test_ref, test_obs)
    assert result == 1.5

def test_previous_err():
    """Test that the controller stores the previous error correctly."""
    controller = PDController()
    test_ref = 10 #assume the reference hight is 10
    test_obs_1 = 8 #assume the 1st observe hight is 8
    test_obs_2 = 9 #assume after the first control iteration, the 2nd observe hight is 9
    result_1st = controller.calculate(test_ref, test_obs_1)
    result_2nd = controller.calculate(test_ref, test_obs_2)
    assert result_2nd == pytest.approx(-0.45)

def test_reset():
    """Test that the reset function of PDController resets the previous error."""
    controller = PDController()
    test_ref = 10
    test_obs = 8
    controller.calculate(test_ref, test_obs)
    controller.reset()
    result = controller.calculate(test_ref, test_obs) #if reset fails, we'll get result = 0.3
    assert result == 1.5 #Black-box / behaviour check