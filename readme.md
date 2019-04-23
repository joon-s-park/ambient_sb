# Ambient Storyboard

This project is developed and maintained by Joon Sung Park and Joshua Reynolds at University of Illinois at Urbana Champaign as a part of CS565 final project. 


## What is in here? 

Ambient Storyboard is built on top of Python's Django web framework. All code written and weaved together for this project is contained within this repo. To see the working version of this project, go to the following URL: 

https://ambient-sb.herokuapp.com/ 

## How to Use

Ambient Storyboard displays a story of a cat named Chi in the background of your browser. If you spend time productively while online (eg. spend less time on social media), the story will progress and you will get to explore the town Chi lives. The images in the storyboard will start blurry, and become crisper as you spend your time more productively.


**How to start**. Simply follow the steps below to start using Ambient Storyboard in less than 10 minutes: 
1. Sign in to Ambient Storyboard with your Gmail/Google account by clicking the "SIGN IN WITH GOOGLE" button above. 
2. Sign up to RescueTime (https://www.rescuetime.com/). Once signed in, travel to the "API and Integrations" section in the menu, and then to "API Key Management" section. Create a new API key, and copy the newly created key. RescueTime will track your online habits to see how productive you have been on a given day. By providing us with its API key, we will be able to use the data collected by RescueTime to progress the story accordingly.
3. Go to settings under the Menu tab in Ambient Storyboard. Paste your API key in the "RescueTime API Key" textbox, and press save.
4. Finally, set Ambient Storyboard as your home tab in your browser and you are ready to go!

## FAQ

**How does RescueTime know whether I am being productive?** RescueTime looks at the sites you go to and measures the amount of the time you spend on those sites. It maintains a list of sites that are often associated with being distracted online, like social media sites. The more time you spend on such sites, the more distracted it will think you are. To get more information, please see RescueTime's documentation (https://www.rescuetime.com/features).

**How does Ambient Storyboard determine when to progress the story?** Based on the data of your online activities such as how much time you spent on social media sites, RescueTime determines your productivity pulse that ranges from 1 to 100 for a given day, where 1 is the least productive, and 100 is the most productive. Ambient Storyboard looks at your productivity pulse from the day before that is provided by RescueTime, and if your pulse is over a certain threshold (eg. defaults at 60), it progresses the story. You can also change the default to set your desired goal for the productivity pulse in the settings, and Ambient Storyboard will progress your story accordingly. 

**Personalization** (eg. I don't consider social media to be distracting!) We understand that you may have different goals and preferences when it comes to being productive online! You can easily change the sites that you consider to be distracting at RescueTime's dashboard. For more information, please see RescueTime's documentation (https://www.rescuetime.com/features). Once you change your preferences there, we will change how your progress is measured in Ambient Storyboard accordingly.

**Chi is cool, but do you offer any other forms of narration?** We do! If you would prefer a narration using static art works instead of a story with a character, please try switchign to the Storyboard set 2 in the Menu > Settings. In this case, a static art work will start off blurry, but get crisper as you progress.


## Credits
The images used in Storyboard Set 1 are from Flying Witch by Chihiro Ishizuka and Katsushi Sakurabi et al. of J.C.Staff.

The images used in Storyboard Set 2 are from Joon Sung Park.

