### KSW_2022_Fall_Program

Your README.md file must include:

(1) Group members name including all Purdue students: e.g., Minji Lee  
(2) Group members univ info: e.g., Purdue University  
(3) Project title  
(4) Research problem statement(s)  
(5) Research novelty (Significance)  
(6) Overview or diagram visual(s)  
(7) Environment settings (Must be very detailed with several steps.) 



### Example:

# 2022 Purdue Beach Cleaning Robot by TEAM C.C
<hr>

 **Project Title**
        
    Post Emergency Power Management for IoT based Precision Agriculture Irrigation System
    Using Cost-Effective Algorithm and Serverless

 **Problem Statement**
    
    The United States has more than 1200 tornadoes per year and almost the highest number of tornadoes in the world. 
    
    Especially, these tornadoes incidences mostly occur in the plains region of the US.
    The tornado occurence area coincides with a large amount of cropland. When such a natural disaster occurs
    the power is cut off, causing a large-scale blackout, and this is not just a problem in cities. 
    
    Recently, as smart farms are created by combining agriculture with IoT, most of the farm work is becoming automated.
    In this situation, if the electricity is cut off, the operation of automation technology of the smart farm will be damaged,
    and the crops will dry while waiting for someone to come and water them.
    
    Therefore, a system that can respond flexibly during a disaster until power is restored is needed. 


 **Novelty**

    1. Develop the existing simple algorithm's concept!
       => 
      
    2. Use LoRa, LoRaWAN with Serverless(FaaS)!
       => 

 **System Overview**
 <p align="center">
   <img src="" alt=""/>
</p>
    
    1. Tomatoes were planted in 4 areas, each with a soil moisture sensor and irrigation tube installed.
    
    2. The crop data is transmitted to the gateway through LoRa communication.
    
    3. The gateway sends the crop data to the Cloud through LoRaWAN communication.
    
    4. When the crop data arrives at the Cloud, store it in the database and apply the devised algorithm.
    
    5. The Cloud sends the irrigation command to the gateway.
    
    6. The irrigation command arrives at the Arduino which operates the irrigation system.

 **Environment Setting**
    
    ✔️Raspberry Pi OS : Ubuntu Server 20.04.5 LTS (64-bit)
    
    ✔️Python version 3.8.10 
    
    ✔Raspberry Pi 4 Model B+ (8GB)
    
    ✔️ROS 2 foxy
  

  **Collaborator**
     
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

