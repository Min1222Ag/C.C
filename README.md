### KSW_2022_Fall_Program

Your README.md file must include:

(3) Project title  
(4) Research problem statement(s)  
(5) Research novelty (Significance)  
(6) Overview or diagram visual(s)  
(7) Environment settings (Must be very detailed with several steps.) 


# 🤖 2022 Purdue Beach Cleaning Robot by TEAM C.C

+ **Project Title**

    Developmental Process and Application of an Eco-Friendly, Autonomous Beach-Cleaning Robot

+ **Problem Statement**
    
    Trash that beach-goers throw away and trash that has been washed up by natural disasters contribute to beach pollution [1]. Beach pollution is harmful to the wildlife that lives on the beach, the residents, tourists, and especially the beach itself. According to the research, implementing all feasible interventions that a human could contribute, approximately 710 million metric tons of plastic waste will occur and affect all ecosystems [2]. In addition, pieces of glass along the beach
could directly hurt people and wildlife [3]. Trash also causes the reduction of tourists and makes around 85% of residents lose up to about 8.5 million dollars since picking up 15 pieces of trash per square meter is the equivalent of roughly 8.5 million dollars [4]. There are multiple different types of beach-cleaning machines that have been developed and implemented due to the limitation of the human ability to clean up beaches. Looking around at robots that are already on the market, many beach-cleaning machines are automatic robots, however, they are not completely automatic in the sense that it requires a human operator. Even though several studies have been conducted on automatic beach-cleaning robots, existing ones have a limited range of only twenty square meters utilizing a scanning range finder, or they are remotely controlled via Bluetooth or autonomously driven following trash detected through a camera.

+ **Novelty**

    🫧 The first Autonomous driving Beach Cleaning Robot with designated GPS points!
       => ABCbot is possible to clean the beach while avoiding obstacles over a wide range.
      
    2. Optimized robot for examine the distance in real time!
       => By combining RPLiDAR, camera, and proximity sensors to examine the distance from the ABCbot in real time, it detects obstacles in front of the robot and uses Google Coral Edge Board to accelerate computing.

    3. An Eco-friendly robot!
       => ABCbot takes power from solar panels and windmills.


+ **System Overview**
 <p align="center">
   <img src="ABCbot.drawio (1).svg" alt="Robot Architecture"/>
</p>
    
    1. Tomatoes were planted in 4 areas, each with a soil moisture sensor and irrigation tube installed.
    
    2. The crop data is transmitted to the gateway through LoRa communication.
    
    3. The gateway sends the crop data to the Cloud through LoRaWAN communication.
    
    4. When the crop data arrives at the Cloud, store it in the database and apply the devised algorithm.
    
    5. The Cloud sends the irrigation command to the gateway.
    
    6. The irrigation command arrives at the Arduino which operates the irrigation system.

+ **Environment Setting**
    
    ✔️Raspberry Pi OS : Ubuntu Server 20.04.5 LTS (64-bit)
    
    ✔️Python version 3.8.10 
    
    ✔️Raspberry Pi 4 Model B+ (8GB)
    
    ✔️ROS 2 foxy
  

+ **Collaborator**
     
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

