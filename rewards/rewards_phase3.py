import gymnasium as gym
from gymnasium import RewardWrapper
import numpy as np

class HardModeRewardWrapper(RewardWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.contact_counts = [1, 1]  # To track leg contact times over an episode
        self.step_counter = 0

    def step(self, action):
        obs, reward, done, truncated, info = self.env.step(action)

        # --- 1. Forward velocity reward ---
        forward_velocity = self.env.unwrapped.hull.linearVelocity[0]
        reward += 0.5 * np.clip(forward_velocity, 0.0, 1.5)

        # --- 2. Penalize excessive vertical movement ---
        vertical_velocity = abs(self.env.unwrapped.hull.linearVelocity[1])
        if vertical_velocity > 0.5:
            reward -= 0.2 * vertical_velocity  # Scaled-down penalty

        # --- 3. Penalize torso instability ---
        hull_angle = abs(self.env.unwrapped.hull.angle)
        reward -= 0.5 * hull_angle

        # Penalize severe torso instability (large hull angle)
        if hull_angle > 0.4:
            reward -= 0.5 * (hull_angle - 0.4)**2  # Scaled penalty

        # --- 4. Reward for overcoming height (jumping obstacles) ---
        if self.env.unwrapped.hull.position[1] > 0.8:  # Height threshold
            reward += 1.0

        # --- 5. Reward balanced leg usage over time ---
        leg_contact = (
            self.env.unwrapped.legs[1].ground_contact or self.env.unwrapped.legs[2].ground_contact,
            self.env.unwrapped.legs[4].ground_contact or self.env.unwrapped.legs[5].ground_contact
        )
        if leg_contact[0]:
            self.contact_counts[0] += 1
        if leg_contact[1]:
            self.contact_counts[1] += 1

        # Every 10 steps, reward balanced leg usage
        self.step_counter += 1
        if self.step_counter % 10 == 0:
            leg_balance = 1 - abs(self.contact_counts[0] - self.contact_counts[1]) / sum(self.contact_counts)
            reward += 0.5 * leg_balance  # Higher reward for balanced usage
            self.contact_counts = [1, 1]  # Reset counts for next interval

        # --- 6. Reward for progress over sloped terrain ---
        if hasattr(self.env.unwrapped, 'on_slope') and self.env.unwrapped.on_slope():
            reward += 0.5  # Reduced from 5.0 to 0.5 for consistency

        # --- 7. Penalize stopping ---
        if forward_velocity < 0.1:
            reward -= 0.5

        # --- 8. Penalize falling ---
        if self.env.unwrapped.game_over:
            reward -= 10.0

        return obs, reward, done, truncated, info