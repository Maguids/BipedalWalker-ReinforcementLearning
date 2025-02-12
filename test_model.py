import gymnasium as gym
from stable_baselines3 import PPO, SAC
from sb3_contrib import TRPO
from rewards import HardModeRewardWrapper

models_dir = "models/PPO_cr"

env = HardModeRewardWrapper(gym.make('BipedalWalker-v3', render_mode="human"))  # continuous: LunarLanderContinuous-v2
env.reset()

model_path = f"{models_dir}/5000000.zip"
model = PPO.load(model_path, env=env)

episodes = 2

for ep in range(episodes):
    obs, info = env.reset()
    done = False
    while not done:
        action, _states = model.predict(obs)
        obs, rewards, trunc, done, info = env.step(action)
        env.render()
        print(ep, rewards, done)
        print("---------------")