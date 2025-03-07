import heapq
import yaml
from chat import evaluate_problem

class Problem:
    def __init__(self, statement, score=0):
        '''Initialize a problem with a statement and an optional score (default is 0)'''
        self.statement = statement  # Problem statement
        self.score = score  # Problem score

    def __lt__(self, other):
        '''Compare problems based on their score (less than comparison)'''
        return self.score < other.score  # Return True if this problem's score is lower than the other's

    def to_dict(self):
        '''Convert the problem to a dictionary format'''
        return {
            "statement": self.statement,  # Problem statement
            "score": self.score  # Problem score
        }
    
    def __repr__(self):
        '''Return a string representation of the problem'''
        return f"Problem (score={self.score}, statement={self.statement[:30]}...)"
        # Show score and first 30 characters of the statement


class Leaderboard:
    def __init__(self, k, yaml_file="output/leaderboard.yaml"):
        '''Initialize with the top k problems and a yaml file for saving the leaderboard'''
        self.k = k  # Number of top problems to track
        self.problems = []  # List of problems in the leaderboard
        self.round = 1  # Round number
        self.yaml_file = yaml_file  # File to save the leaderboard

    def update_leaderboard(self, problem):
        '''Update the leaderboard with a new problem'''
        if len(self.problems) < self.k:
            # Add the problem if there are fewer than k problems
            heapq.heappush(self.problems, (problem.score, problem))
        else:
            # Replace the problem if there are already k problems
            heapq.heappushpop(self.problems, (problem.score, problem))

    def get_top_problems(self):
        '''Get the top problems sorted by score (descending)'''
        return sorted(self.problems, key=lambda x: -x[0])  # Sort problems by score in descending order
    
    async def save_to_yaml(self):
        '''Save the leaderboard to a yaml file asynchronously'''
        problems_sorted = sorted(self.problems, key=lambda x: x[0], reverse=True)  # Sort problems by score
        
        # Prepare data for the current round
        round_data = {
            f"Round {self.round}": {
                "problems": [p.to_dict() for _, p in problems_sorted]  # Convert each problem to dictionary format
            }
        }
        self.round += 1  # Increment round number
        
        # Save the data to the yaml file asynchronously
        with open(self.yaml_file, "a", encoding="utf-8") as file:
            yaml.dump(round_data, file, default_flow_style=False, allow_unicode=True)
          
    async def evaluate(self, problems, args):
        '''Evaluate and update leaderboard for a list of problems'''
        for problem in problems:
            # Evaluate score for each problem
            problem.score = float(evaluate_problem(problem.statement, args.agent))
            # Update leaderboard with the problem
            self.update_leaderboard(problem)  
        # Save leaderboard to yaml file
        await self.save_to_yaml()


        
