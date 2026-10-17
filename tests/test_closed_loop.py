import numpy as np

from uuv_mission.dynamic import ClosedLoop, Mission, Submarine


class RecordingController:
    """Returns a constant action and records every call made by ClosedLoop."""

    def __init__(self, action=0.0):
        self.action = action
        self.calls = []

    def reset(self):
        self.calls.append("reset")

    def compute_action(self, observation, reference):
        self.calls.append((observation, reference))
        return self.action


def make_mission(T=20):
    reference = np.linspace(0, 5, T)
    return Mission(reference, reference + 10, reference - 10)


def test_simulate_resets_then_passes_observation_and_reference():
    mission = make_mission()
    controller = RecordingController()
    trajectory = ClosedLoop(Submarine(), controller).simulate(mission, np.zeros(20))

    assert controller.calls[0] == "reset"
    observations, references = zip(*controller.calls[1:])
    np.testing.assert_allclose(references, mission.reference)
    np.testing.assert_allclose(observations, trajectory.position[:, 1])


def test_simulate_applies_controller_action_to_plant():
    mission = make_mission()
    disturbances = np.random.default_rng(0).normal(0, 0.5, 20)
    trajectory = ClosedLoop(Submarine(), RecordingController(action=1.0)).simulate(mission, disturbances)

    expected = Submarine()
    for t in range(20):
        np.testing.assert_allclose(trajectory.position[t], expected.get_position())
        expected.transition(1.0, disturbances[t])


def test_simulate_resets_controller_on_every_run():
    controller = RecordingController()
    closed_loop = ClosedLoop(Submarine(), controller)
    closed_loop.simulate(make_mission(), np.zeros(20))
    closed_loop.simulate(make_mission(), np.zeros(20))

    assert controller.calls.count("reset") == 2
    assert controller.calls[21] == "reset"
