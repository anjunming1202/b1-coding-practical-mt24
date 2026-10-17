class PDController:
    def __init__(self, kp: float = 0.15, kd: float = 0.6):
        self.kp = kp
        self.kd = kd
        self.previous_err: float = 0.0

    def compute_action(self, obs: float, ref: float):
        err = ref - obs
        de = err - self.previous_err
        self.previous_err = err
        return self.kp * err + self.kd * de

    def reset(self):
        self.previous_err: float = 0.0
