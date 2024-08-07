# AI-agent for action-RPG Path of Exile
**_Non-profit, for educational purposes only._** <br>

The final goal of the project is to create an easily adaptable product for full cycle of creating AI-agents,
that can play modern computer games while relying solely on information available from the screen capture.

## Current progress
![](https://geps.dev/progress/60)
- [x] Data gathering 
- [x] Data preparation and storage 
- [x] Model creation and training 
- [x] Model testing in-game
- [ ] Fine tuning of models
- [ ] Fully capable AI-agent 

## Explanation and usage
### General
<p> 
  Repository provides source code for everything I used to gather and prepare the dataset for training several CNN models.<br>
  Currently I am actively working on documenting what is happening here, because till now it was exposed only to small team.<br>
  I decided to not provide existing trained models, because usage of such software is against PoE's ToS. However I am planning on
  showing the actual performance in video format(this will take some time).

### Problem
  The goal is to create an AI-agent which is capable of traversing and killing enemies in procedurely generated environments inside PC game Path of Exile, 
  specifically so called maps.

### AI-agent architecture
  The idea is to use CNN classification model based on logistic regression to identify two cases: whether it's time to attack or to explore the area. 
  After that image is passed to next round based on previous decision. In second round given same image similar CNNs predict mouse X and Y location. 
  Attack and Explore models are trained on different datasets regarding specific in-game tasks. Having predicted mouse position and required action,
  it is sent to the game via custom module move_ctypes(cici) encycling the process.

### PyTorch and TensorFlow dilemma
  Because Path of Exile is very demanding game, it pretty much requires to be ran on Windows, so I gotta come up with solution for both fast and reliable
  method of running the game while keeping script with predictions going on setup which I have(GTX 1060, i7-6700). <br>

  Generally there are two approaches, server - client architecture, where server serves as computing unit, and client uses server's predictions for sending inputes and new screenshots,
  or on-client computation, which is much more demanding, however much easier to apply. Given I already had a previous experience with server-client, and it went very sour, I decided 
  to stop on client only approach.<br>

  Before starting this project I have used both TF and Torch, however I felt comfier using tensorflow, and that decision was catastrophic. It's borderline impossible to run tensorflow
  on GPU locally, I've tried to use previous python versions, WSL2, Conda Envs, everything suggested for Windows native, and had very little success. After one week of brain rot from
  setuping different envs for tf, and have them break the very next second, I have dropped my attempts to implement tf for this task. <br>

  To be fair, precision of tf models were decent, especially classification using ResNet. However speed of predictions using only CPU wasn't enough to cut it, and GPU just didn't want
  to run or stopped predicting after making 1 loop withouth any errors. <br>

  Finally, I've tried to train the models on PyTorch and it snapped instantly, no problems at all. Currently project is being driven around it(tf notebooks are left for perhaps any future
  reference)
### Real time image extraction
### Image preparation, labeling and storaging
### Techniques used for achieving better training results(with examples)
</p>
