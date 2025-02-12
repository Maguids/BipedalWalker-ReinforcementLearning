import multiprocessing
import os
from sys import argv
from stable_baselines3 import A2C, PPO, SAC, TD3  # Algoritmos do Stable Baselines3
from sb3_contrib import TQC, TRPO  # Algoritmos do sb3-contrib
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import SubprocVecEnv
from rewards import HardModeRewardWrapper
import gymnasium as gym

env_id = "BipedalWalker-v3"

TIMESTEPS = 500000
models_dir = "models"
logdir = "logs"


def latest_model(algorithm):
    """Busca o último modelo salvo de um algoritmo"""
    models = [int(model.split(".")[0]) for model in os.listdir(f"{models_dir}/{algorithm}")]
    models.sort()
    return f"{models_dir}/{algorithm}/{models[-1]}.zip"


def train_model(algo, algo_name, policy, n_envs=os.cpu_count(), use_gpu=False):
    """Treina o modelo para o algoritmo especificado"""
    
    # Configurar GPU ou CPU com base na escolha do algoritmo
    if use_gpu:
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Usar GPU (assumindo que você tenha pelo menos uma GPU)
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Forçar uso de CPU

    # Criar ambiente
    env = make_vec_env(lambda: HardModeRewardWrapper(gym.make(env_id, hardcore = True)), 
                       n_envs=n_envs, 
                       vec_env_cls=SubprocVecEnv, 
                       vec_env_kwargs=dict(start_method='fork'))

    # Certificar-se que o diretório do modelo existe
    if os.path.exists(f"{models_dir}/{algo_name}"):
        if os.listdir(f"{models_dir}/{algo_name}"):

            model_path = latest_model(algo_name)
            model = algo.load(model_path, env=env, reset_num_timesteps=False)
            iters = int(int(model_path.split("/")[2].split(".")[0]) / TIMESTEPS)
        else:
            model = algo(policy, env, verbose=1, tensorboard_log=logdir)
            iters = 0
    else:
        os.makedirs(f"{models_dir}/{algo_name}")
        model = algo(policy, env, verbose=1, tensorboard_log=logdir)
        iters = 0

    while True:
        iters += 1
        model.learn(
            total_timesteps=TIMESTEPS,
            progress_bar=True,
            reset_num_timesteps=False,
            tb_log_name=algo_name
        )
        model.save(f"{models_dir}/{algo_name}/{TIMESTEPS * iters}")
        if iters * TIMESTEPS >= 10000000:
            break


def train_process(algo, algo_name, policy, n_envs, use_gpu):
    """Função de subprocesso para treinar modelos simultaneamente"""
    train_model(algo, algo_name, policy, n_envs=n_envs, use_gpu=use_gpu)


def main():
    try:
        # Verifica se a escolha do GPU/CPU foi especificada
        if len(argv) != 1:
            raise ValueError("No arguments given. Please specify the GPU/CPU setup.")

        # Criação dos diretórios, caso não existam
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)



        # Lista de algoritmos e seus parâmetros
        algorithms = [
            #{"algo": A2C, "name": "A2C", "policy": "MlpPolicy", "n_envs": 1, "use_gpu": False},   # CPU
            #{"algo": PPO, "name": "PPO", "policy": "MlpPolicy", "n_envs": 20, "use_gpu": False},   # CPU
            #{"algo": SAC, "name": "SAC", "policy": "MlpPolicy", "n_envs": 10, "use_gpu": True},    # GPU
            #{"algo": TD3, "name": "TD3", "policy": "MlpPolicy", "n_envs": 2, "use_gpu": False},    # CPU
            #{"algo": TQC, "name": "TQC", "policy": "MlpPolicy", "n_envs": 50, "use_gpu": False},   # CPU
            {"algo": TRPO, "name": "TRPO", "policy": "MlpPolicy", "n_envs": 180, "use_gpu": False},   # GPU
        ]

        # Criação de subprocessos para rodar os algoritmos simultaneamente
        processes = []
        for algo_config in algorithms:
            p = multiprocessing.Process(target=train_process, args=(
                algo_config["algo"],
                algo_config["name"],
                algo_config["policy"],
                algo_config["n_envs"],
                algo_config["use_gpu"]  # Passa a escolha de GPU/CPU diretamente do dicionário
            ))
            p.start()
            processes.append(p)

        # Aguardar todos os subprocessos terminarem
        for p in processes:
            p.join()

        print("Todos os treinamentos foram concluídos.")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
