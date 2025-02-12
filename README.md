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

![multimedia1](https://github.com/user-attachments/assets/3f9b8388-2a3c-4fe1-953a-76a7b5ce3b4f)

<br>

## The Interface:
When running 'interface.py' you will get to choose the size of the environment. Then you can do the following by pressing the controls:
B + Click -> You create a **bin** on the square you clicked;
T + Click -> You create a **truck** on the square you clicked;
R + Click -> You create a **roadblock** on the square you clicked;
1 -> You set traffict level to 1;
2 -> You set traffict level to 2;
3 -> You set traffict level to 3;
4 -> You set traffict level to 4;
5 -> You set traffict level to 5;
0 -> You set traffict level to 0 (clear all traffic);
S -> You **START** the program

**Notes:** 
- When you create traffic you only define how much traffic is going to be created, you can't choose where as it is generated randomly.
- Traffic is represented as an orange line
- Roadblocks are red squares
-  The truck with a semi red square on top of it is broken by a random time, when it is operational again the square will disappear. 
- Trucks can break down at any time and randomly, you can't controle it. 
- The blue square is the central
- On the right side you have the status were you can see de capacity of each bin (the color changes accordingly) and the capacity of trucks and its fuel

<br>

<p align="center">
  <img width="850" height="400" src="https://github.com/user-attachments/assets/4a73e465-0e3f-4f76-9eaa-ce93dcd89b8b">


<br>

## About the repository:

- Assignment.pdf ➡️Project statement
- bin_agent.py ➡️ The code of the bin agent;
- truck_agent.py ➡️ The code of the truck agent;
- environment.py ➡️ The code of the environment;
- interface.py ➡️ The code of the interface;
- prosody.txt ➡️ How your 'prosody.cfg.lua' should be;
- Multi-Agent-Autonomous-Waste-Collection-System.pdf ➡️ The tests and its results and more info about what was done.

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
