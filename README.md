### KSW_2022_Fall_Program

Your README.md file must include:

(3) Project title  
(4) Research problem statement(s)  
(5) Research novelty (Significance)  
(6) Overview or diagram visual(s)  
(7) Environment settings (Must be very detailed with several steps.) 


## 🤖 2022 Purdue Beach Cleaning Robot by TEAM C.C


#### 🌊 Project Title

    Developmental Process and Application of an Eco-Friendly, Autonomous Beach-Cleaning Robot

#### 🌊 Problem Statement
    
      In 2016, the United States was responsible for 42 million metric tons of plastic waste, which made it the largest contributor
    in the world. The U.S is also ranked 3rd in the world when it comes to depositing pollution onto its own shorelines. There is
    an estimated 95,000 miles of shoreline in the United States as well as an estimated 90,000 beaches across the country. To say  
    pollution and waste are an issue for the beaches, is an understatement.

      Litter on the beaches affect not only water, but also the wildlife, local residents, and even the economic state of the area.  
    Trash can make living conditions for any living organism, unsuitable. This happens when a turtle mistakes a plastic bag as a  
    jellyfish, causing the turtle to consume the trash because jellyfish are a part of a turtle's diet. When pollution infects
    a beach, it make it look unpleasant, which in turn would turn off tourists from wanting to visit the beach while also  
    potentially making local residents want to move from the area. These two instances combined can have a devastating impact on  
    the economy as tourism is a significant portion of the U.S's economy. 

      There is no easy solution to this problem, however the development of a self-driving robot that can gather and dispose of  
    trash on its own is a good start.

#### 🌊 Novelty

    The first Autonomous driving Beach Cleaning Robot with designated GPS points!
       => ABCbot is possible to clean the beach while avoiding obstacles over a wide range.
      
    Optimized robot for examine the distance in real time!
       => By combining RPLiDAR, camera, and proximity sensors to examine the distance from the ABCbot in real time, it detects
          obstacles in front of the robot and uses Google Coral Edge Board to accelerate computing.

    An Eco-friendly robot!
       => ABCbot takes power from solar panels and windmills.


#### 🌊 System Overview
<p align="center">
   <img src="ABCbot_presentation.drawio.png" alt="Robot Architecture" height="300"/>
</p>

    1. One raspberry pi 4B is used for the driving unit equipping GPS, magnetometer sensor, DC motors and relay, and proximity sensors.
    
    2. Another raspberry pi 4B is utilized as a detection unit arming PiCam and LiDAR.
    
    3. Two raspberry pi 4Bs communicate with each other through ROS2 Foxy.
    
    4. All the raspberry pi 4Bs and sensors have power supplied by a solar panel and a wind turbine.
    
<p align="center">    
    <img src="control flow2.drawio.png" alt="Flow Diagram"/>
</p>

    1. .
    
    2. .
    
    3. .
    
    4. .
    
#### 🌊 Environment Setting
    
    - Raspberry Pi OS : Ubuntu Server 20.04.5 LTS (64-bit)
    
    - Python version 3.8.10 
    
    - Raspberry Pi 4 Model B+ (8GB)
    
    - ROS 2 foxy
  

#### 🌊 Collaborator
     
       Eunmin Kim
       - Dankook Univeristy
       - Majoring in Industrial Security
       - maexc834@naver.com
       - https://github.com/Min1222Ag
       
       Booyong Kim
       - Sangmyung University
       - Majoring in Computer Science
       - hapata1120@gmail.com
       - https://github.com/KBY538
      
       Seoyeong Lee
       - Daegu Catholic University
       - Majoring in Computer Engineering
       - lsyoung66@naver.com
       - https://github.com/lsyoung66
       
       Hanbyeol Lee
       - Chung-Ang University
       - Majoring in Computer Science and Engineering
       - yhb1834@cau.ac.kr
       - https://github.com/yhb1834
    
       Jeeyoung Oh
       - Chung-ang University
       - Majoring in Computer Science and Engineering
       - jeeyoung9907@cau.ac.kr
       - https://github.com/ohjeeyoung
    
       Caleb Ikalina
       - Purdue University
       - Majoring in Computer and Information Technology, Forensic Sciences
       - maxli32145@gmail.com
       - cikalina@purdue.edu
       - https://github.com/CalebIkalina

