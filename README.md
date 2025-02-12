# BipedalWalker Reinforcement Learning

This project was developed for the "Introduction to Intelligent Autonomous Systems" course and aims to **develop a reinforcement learning agent using Gymnasium** environment as a base. The task is to **introduce specific changes or customizations to the environment** and **train the BipedalWalker-v3 using the Stable Baselines library**. The goal is to assess how these **changes impact** the agent's learning process and performance. First Semester of the Third Year of the Bachelor's Degree in Artificial Intelligence and Data Science.

<br>

## Programming Language:

<div style = "display: inline_block"><br/>
  <img align="center" alt="python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</div><br/>

<br>

## Requirements:

	- stable-baselines3[extra]
	- swig
	- gymnasium[box2d]
	- sb3-contrib

<br>

## The Standard BipedalWalker:
<p align="center">
  <img width="850" height="400" src="https://github.com/user-attachments/assets/3a36e847-0a9e-434d-b03c-02c67f75817a">
</p>

**States:**
The  state  is a continuous  vector  of 24 dimensions  wich  include:
- Angle and angular velocity of the hull (main body): 2 points.
- Horizontal and vertical hull speed: 2 points.
- Joint angles and leg angular velocities: 8 points (4 joints x 2 points each).
- Ground contact sensors on the legs: 2 values ​​(indicating whether each leg is in contact with the ground).
- Information on the terrain ahead (LIDAR sensors): 10 points (terrain readings to anticipate obstacles).

**Rewards:**
Reward is given for moving forward, totalling 300+ points up to the far end. If the robot falls, it gets -100. Applying motor torque costs a small amount of points.

**Percepts:**
The agent sees everything it needs to (state = perceptions), as the environment is fully observable, eliminating the need to infer hidden information or deal with noise.

**Actions:**
Actions are motor speed values in the [-1, 1] range for each of the 4 joints at both hips and knees.

<br>

## The Project:
At an early stage, we started by trying to decide which RL algorithms would be best suited for BipedalWalker-v3, so we tested several different algorithms in normal mode with 5M timesteps:

<p align="center">
  <img width="850" height="400" src="https://github.com/user-attachments/assets/d38bfb48-419a-4f29-b20a-912b779c9c68">
</p>

When analyzing the results, we chose to use **PPO**, **SAC** and **TRPO**.

<br>

### First Phase:
Initially, we decided to **test small rewards** to understand the **impact each of them** had and whether their use was justified or not, having trained the models with **30M timesteps**. For this we made two tests:

| Tests | Rewards | Penalties | Video |
| :- | :- | :- | :- |
|Test 1 | - Overcome steep terrain | - Vertical sudden moves (ex: falling) <br> - Severe instability (ex: torso inclination) | <img width="300" height="200" src="https://github.com/user-attachments/assets/1e3b8145-3318-46ee-8318-d16fcef7b98d"> |
| Test 2 | - Alternate feet | - Vertical sudden moves (ex: falling) | <img width="300" height="200" src="https://github.com/user-attachments/assets/3f5c17bf-9775-4e35-9160-e42228544a17"> |

<br>

### Second Phase:
After detecting the initial errors, we realized that we should encourage the agent to walk forward and remove the alternating use of both feet:

**Rewards:**
- Overcome steep terrain
- Moving forward

**Penalties:**
- Vertical sudden moves (ex: falling)
- Severe instability (ex: torso inclination)
- Stands still for a long time or stops moving
- Agent fails

**Videos:**

| PPO | TRPO |
| :-: | :-: |
| <img width="300" height="200" src=""> | <img width="300" height="200" src="https://github.com/user-attachments/assets/f131fba1-c6ae-46eb-b7bb-e9ef063b2616"> |

| SAC | CONTROL |
| :-: | :-: |
| <img width="300" height="200" src="https://github.com/user-attachments/assets/e0cf5cc0-5fa5-4a8c-af59-6628ece6672f"> | <img width="300" height="200" src="https://github.com/user-attachments/assets/230e8816-ee29-4d46-a064-cabef5660019"> |

### Third Phase:
In an attempt to further improve the second phase, we decided to do a third test by changing the rewards again and truing to correct the minor errors detected in the previous phase.

**Rewards:**
- Overcome steep terrain
- Moving forward
- Lifting its legs from the ground
- Using each leg the same number of times

**Penalties:**
- Vertical sudden moves (ex: falling)
- Severe instability (ex: torso inclination)
- Stands still for a long time or stops moving
- Agent fails

**Videos:**

| PPO | TRPO |
| :-: | :-: |
| <img width="300" height="200" src="https://github.com/user-attachments/assets/0db319d2-1692-408e-86d1-7f7cb7db89bc"> | <img width="300" height="200" src="https://github.com/user-attachments/assets/ff82d86f-788e-421e-8c27-e2fe8ccc892a"> |

| SAC | CONTROL |
| :-: | :-: |
| <img width="300" height="200" src="https://github.com/user-attachments/assets/6ffaee9f-6481-48d0-8d9e-6720e48f5aa3"> | <img width="300" height="200" src="https://github.com/user-attachments/assets/ef461159-1d1d-42da-82f6-18eca8472ed0"> |


## Other Tests:
In addition to the tests demonstrated above, we also performed two other tests:

### Feet VS No Feet:
In order to try to understand if the agent would move better with feet, we **created an agent with feet**.

<p align="center">
  <img width="700" height="250" src="https://github.com/user-attachments/assets/2fce22f6-0b0d-49b5-a912-f197f4c39033">
</p>

### Hiperparameter Tunning


<br>

## About the repository:

- rewards ➡️ Its a folder with python files with the different rewards that were used;
- Assignment.pdf ➡️ Project statement;
- BipedalWalker.pptx ➡️ Its a Powerpoint with information about the work developed;
- ExtraBW.pptx ➡️ Its a Powerpoint with some extra information about the work developed (graphs, videos...);
- bipedal_walker_custom.txt ➡️ If you wanna try the BipedalWalker with feet this is what you have to use;
- rewards_train.py ➡️ The code for trainning the agent with rewards;
- test_model.py ➡️ The code used to test the agents;
- train_models.py ➡️ The code used to train the agents.

Note:
- When trainning agents we are training several algorihtms at the same time, you can choose which ones you are using and how many environments at the same time for each algorithm, and if you are using CPU or GPU for each algorithm.

<br>

## Link to the course: 

This course is part of the **<u>first semester</u>** of the **<u>third year</u>** of the **<u>Bachelor's Degree in Artificial Intelligence and Data Science</u>** at **<u>FCUP</u>** and **<u>FEUP</u>** in the academic year 2024/2025. You can find more information about this course at the following link:

<div style="display: flex; flex-direction: column; align-items: center; gap: 10px;">
  <a href="https://sigarra.up.pt/fcup/pt/ucurr_geral.ficha_uc_view?pv_ocorrencia_id=529876">
    <img alt="Link to Course" src="https://img.shields.io/badge/Link_to_Course-0077B5?style=for-the-badge&logo=logoColor=white" />
  </a>

  <div style="display: flex; gap: 10px; justify-content: center;">
    <a href="https://sigarra.up.pt/fcup/pt/web_page.inicial">
      <img alt="FCUP" src="https://img.shields.io/badge/FCUP-808080?style=for-the-badge&logo=logoColor=grey" />
    </a>
    <a href="https://sigarra.up.pt/feup/pt/web_page.inicial">
      <img alt="FEUP" src="https://img.shields.io/badge/FEUP-808080?style=for-the-badge&logo=logoColor=grey" />
    </a>
  </div>
</div>
