# Parliament Agents simulation
Framework to simulate parliaments behaviour using SPADE.


## Installation

The application relies on SPADE as base Agent framework so it's necessary to have it installed before launching it. 
To install simply use requirements file using following command:
```cmd
$ pip install -r requirements.txt
```

## Running

### Accounts
There are 3 distinct agents used within the system:
* Parliament Agent
* Voting System Agent
* European Parliament Agent

All 3 need their own JIDs so therefore it is necessary all of them have their own Jabbim accounts. Each only needs one account, with exception of
Parliament Agent where it depends on how many different parties are desired to be in the simulation.
Any Jabbim server can be used and in provided example we used https://www.jabbim.pl/.
Use "ParliamentarianAgentAccounts.txt" as your password file as example provided by us. Account name and password for Parliamentarian Agents are automatically read from it.
Remember not to commit this file to your own repository!

### Data files

Simulation runs based on provided data files and they are instrumental in running it. 
There are several example files provided by us to show proper structure on how we read them (mostly due to simplicity reasons).

1. StartUnionState - contains start of the union with all areas of concern and their values.
2. ParlimentParties.json - contains different parties and union state that they are most interested about. 
3. InterestAreas.txt - contains list of all possible interest areas (previous files need to match this one).
4. sample_200_dossiers.json - contains list of example dossiers that were passed by European Union Parliament.

Should you want to change any data file names, simply edit [main.py](https://github.com/KasprzykM/parliament-agents/blob/master/parliament-agents/main.py) in:
```python
if __name__ == '__main__':
    simulation = Simulation()
    simulation.setup("InterestAreas.txt", "ParliamentarianAgentAccounts.txt", "resources/ParlimentParties.json",
                     "resources/StartUnionState")
    simulation.start_voting("resources/Statutes.json")
```

### Launch

If you do not wish to put your own configuration simply run:
```cmd
$ python main.py
```

Alternatively, first set up all the necessary date and then run the previous command.

## Results

There is a lot of log output and there are 2 ways of looking at the results:

1. Looking at message logs of communications between agents. It can be read directly from console or simply uncomment line that in [main.py](https://github.com/KasprzykM/parliament-agents/blob/master/parliament-agents/main.py) that says:
    ```python
    # log_redirect()  # uncomment if you wish to scubadive logs
    ```
    This produces file named "parliament_log.txt" that contains all messages.

2. After simulation ends, results of all the votes and their subjects is stored in "voting_results.json" which contains information like who voted for what and what was the subject of the vote.


## Additional information

Unfortunately full documentation is only available in polish and there are no plans of changing that. You can read them here: [docs](https://docs.google.com/document/d/1BPgQ7d98cPj9B2yDgQTq_-n52QZCi1ovQAEQRQS3DAo/edit?fbclid=IwAR0gQNu2NyMvzFttFbCxxhftcW3LnzHXYH_lyg3IUCUI5puc47XrVvaxFPw#).
It contains much more in depth explanation on how the system works as well as analysis of results of the simulation.