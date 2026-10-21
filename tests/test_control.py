from uuv_mission.control import PDController
import pytest

def test_calculate(): 
    """Test the calculate function of PDController"""
    controller = PDController()
    test_ref = 10
    test_obs = 8
    result = controller.compute_action(test_obs, test_ref)
    assert result == 1.5

def test_previous_err():
    """Test that the controller stores the previous error correctly."""
    controller = PDController()
    test_ref = 10 #assume the reference hight is 10
    test_obs_1 = 8 #assume the 1st observe hight is 8
    test_obs_2 = 9 #assume after the first control iteration, the 2nd observe hight is 9
    result_1st = controller.compute_action(test_obs_1, test_ref)
    result_2nd = controller.compute_action(test_obs_2, test_ref)
    assert result_2nd == pytest.approx(-0.45)

def test_reset():
    """Test that the reset function of PDController resets the previous error."""
    controller = PDController()
    test_ref = 10
    test_obs = 8
    controller.compute_action(test_obs, test_ref)
    controller.reset()
    result = controller.compute_action(test_obs, test_ref) #if reset fails, we'll get result = 0.3
    assert result == 1.5 #Black-box / behaviour check

def test_compute_action_accepts_interface_keywords():
    """Test that PDController matches the Controller interface parameter names."""
    controller = PDController()
    result = controller.compute_action(observation=8, reference=10)
    assert result == 1.5
