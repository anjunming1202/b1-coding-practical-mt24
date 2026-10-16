from pathlib import Path

import numpy as np

from uuv_mission.dynamic import Mission
from uuv_mission.terrain import write_mission_to_csv

DATA_FILE = Path(__file__).parent.parent / "data" / "mission.csv"


def test_from_csv_loads_columns_in_order():
    mission = Mission.from_csv(DATA_FILE)
    assert mission.reference.shape == (100,)
    assert (mission.reference[0], mission.cave_height[0], mission.cave_depth[0]) == (0.0, 30.0, -30.0)


def test_from_csv_round_trip(tmp_path):
    original = Mission.random_mission(50, 5)
    write_mission_to_csv(original, tmp_path / "mission.csv")
    loaded = Mission.from_csv(tmp_path / "mission.csv")
    for field in ("reference", "cave_height", "cave_depth"):
        np.testing.assert_allclose(getattr(loaded, field), getattr(original, field))
