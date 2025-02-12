import gymnasium as gym
from gymnasium import RewardWrapper

class HardModeRewardWrapper(RewardWrapper):
    def __init__(self, env):
        super().__init__(env)

    def reward(self, reward):
        # Recompensa por progresso sobre terrenos inclinados
        if hasattr(self.env.unwrapped, 'on_slope') and self.env.unwrapped.on_slope():
            reward += 5.0

        # Penalizar movimentos verticais exagerados
        vertical_movement = abs(self.env.unwrapped.hull.linearVelocity[1])
        if vertical_movement > 0.5:
            reward -= 2.0 * vertical_movement

        # Penalizar instabilidade severa (inclinação maior que 0.4 rad)
        hull_angle = abs(self.env.unwrapped.hull.angle)
        if hull_angle > 0.4:
            reward -= 5.0 * (hull_angle - 0.4)**2

        return reward
