import gymnasium as gym
from gymnasium import RewardWrapper
import numpy as np

class HardModeRewardWrapper(RewardWrapper):
    def __init__(self, env):
        super().__init__(env)

    def reward(self, reward):
        """
        Modify the environment reward based on custom rules. Rewards and penalties
        are scaled to be consistent with the ones in the image.
        """
        #(forward movement incentive) ---
        forward_velocity = self.env.unwrapped.hull.linearVelocity[0]  # Forward velocity
        reward += 0.5 * np.clip(forward_velocity, 0.0, 2.0) # Incentive for forward motion

        # Penalty for staying still (low movement)
        if forward_velocity < 0.1:
            reward -= 0.2  # Small penalty

        # Penalty for torso inclination (scaled down)
        hull_angle = abs(self.env.unwrapped.hull.angle)
        reward -= 0.3 * hull_angle  # Consistent with the image's scale

        # High penalty for episode termination (falling), scaled down
        if self.env.unwrapped.game_over:  # Assuming done == True means fall
            reward -= 15.0  # Scaled to fit with the other rewards

        # --- Hard mode adjustments (scaled down) ---
        # Reward for progress over sloped terrain
        if hasattr(self.env.unwrapped, 'on_slope') and self.env.unwrapped.on_slope():
            reward += 0.5  # Reduced from 5.0 to 0.5 for consistency

        # Penalize excessive vertical movement (scaled down)
        vertical_movement = abs(self.env.unwrapped.hull.linearVelocity[1])
        if vertical_movement > 0.5:
            reward -= 0.2 * vertical_movement  # Reduced penalty

        # Penalize severe torso instability (large hull angle)
        if hull_angle > 0.4:
            reward -= 0.5 * (hull_angle - 0.4)**2  # Reduced penalty

        return reward
