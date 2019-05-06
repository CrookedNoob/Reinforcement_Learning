#!/usr/bin/env python
# coding: utf-8

# In[53]:


import gym
import numpy as np
from flask import Flask
import json

env= gym.make('CartPole-v1')


# In[48]:


def play(env, policy):
    observation= env.reset()
    
    done=False
    score=0
    observations=[]
    
    for _ in range(5000):
        observations += [observation.tolist()]
        
        if done:
            break
            
            
        outcome= np.dot(policy, observation)
        action= 1 if outcome> 0 else 0
        
        
        observation, reward, done, info= env.step(action)
        score+= reward
        
    return score, observations


# In[49]:


max= (0, [], [])


# In[50]:


for _ in range(100):
    policy= np.random.rand(1, 4)
    score, observations= play(env, policy)
    
    if score> max[0]:
        max= (score, observations, policy)
        
print("max score ", max[0], '\n')    


# In[52]:


scores=[]

for _ in range(100):
    score, _ =play(env, max[2]) 
    scores += [score]
    
print("Avg Score (100 trials): ", np.mean(scores))


# In[ ]:


print("Starting Replay...")

app= Flask(__name__, static_folder='.')

@app.route('/data')
def data():
    return json.dumps(max[1])

@app.route('/')
def route():
    return app.send_static_file('./index.html')
    
app.run(host='0.0.0.0', port= '3000')


# In[ ]:




