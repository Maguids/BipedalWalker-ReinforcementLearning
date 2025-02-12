import gymnasium as gym
from gymnasium import RewardWrapper

class HardModeRewardWrapper(RewardWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.last_foot_contact = None

    def reward(self, reward):
        # Alternância dos pés
        left_leg_contacts = self.env.unwrapped.legs[0].contacts
        right_leg_contacts = self.env.unwrapped.legs[1].contacts

        left_foot_contact = any(contact for contact in left_leg_contacts)
        right_foot_contact = any(contact for contact in right_leg_contacts)

        if left_foot_contact and not right_foot_contact:
            if self.last_foot_contact == 'right':
                reward += 1.0
            self.last_foot_contact = 'left'
        elif right_foot_contact and not left_foot_contact:
            if self.last_foot_contact == 'left':
                reward += 1.0
            self.last_foot_contact = 'right'

        # Penalizar movimentos verticais bruscos
        vertical_movement = abs(self.env.unwrapped.hull.linearVelocity[1])
        if vertical_movement > 0.5:
            reward -= 1.0 * vertical_movement

        return reward