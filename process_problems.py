import argparse
import datetime
import functools
import os
import re
import shutil
import concurrent.futures
import aiofiles
import asyncio
from chat import chat_completion
from ranking import Problem, Leaderboard
import logging

logging.basicConfig(level=logging.INFO,  # Define the logging level
                    format='%(asctime)s - %(levelname)s - %(message)s',  # Message format
                    handlers=[logging.StreamHandler()])  # Output to console

def load_problems():
    '''Loads problems from a text file and converts them into Problem objects.'''
    file_path = "problems/problems.txt"
    problems = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read each line, strip spaces, and create a Problem object
            for line in file.readlines():
                statement = line.strip()
                if statement:  # Check if the line is not empty
                    problem = Problem(statement)
                    problems.append(problem)
    except FileNotFoundError as e:
        logging.error(f"The file {file_path} was not found: {e}")
        exit()
    return problems

def mutate_problem(problem, strategy, agent):
    """Applies a mutation to a problem using the OpenAI API."""
    template_path = f'prompts/mutations/{strategy}.txt'
    
    if not os.path.exists(template_path):
        raise ValueError(f"Mutation template does not exist for: {strategy} in {template_path}")
    
    with open(template_path, 'r', encoding='utf-8') as file:
        prompt = file.read() + problem.statement
    
    # print(f"prompt:{prompt}")   
    response = chat_completion(prompt, agent)
    # print(f"response:{response}")
    return response

async def save_mutations(args, mutated_problems, datetime):
    '''Save mutated problems to an output file asynchronously.'''
    output_dir = os.path.join(os.getcwd(), "output", "output_" + datetime, args.output)    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    existing_files = [f for f in os.listdir(output_dir) if f.startswith(args.output) and f.endswith(".txt")]
    output_file = os.path.join(output_dir, f"{args.output}_{len(existing_files) + 1}.txt")

    # Write mutated problems to the output file
    async with aiofiles.open(output_file, 'w', encoding='utf-8') as file:
        await file.write("\n".join(f"Problem {i+1}: {problem.statement}" for i, problem in enumerate(mutated_problems)))

    logging.info(f"Mutations saved in {output_file}")

def clear_ouput():
    '''Clears the output folder and resets leaderboard file.'''
    date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}")
    output_dir = os.path.join(os.getcwd(), "output")
    leaderboard_path = "output/leaderboard.yaml"

    if os.path.exists(output_dir):
        for folder in os.listdir(output_dir):
            folder_path = os.path.join(output_dir, folder)
            if os.path.isdir(folder_path) and date_pattern.search(folder):
                shutil.rmtree(folder_path)
        os.remove(os.path.join(output_dir, "leaderboard.yaml"))

        if os.path.exists(leaderboard_path):
            with open(leaderboard_path, 'w', encoding='utf-8') as file:
                pass  # Clear the file content
        else:
            # If the file doesn't exist, create it empty
            with open(leaderboard_path, 'w', encoding='utf-8') as file:
                pass  # Also creates empty

    else:
        logging.error("Folder 'output' does not exist.")

def mutate_with_index(args_tuple, args):
    '''Mutate a problem with a given strategy and return a new Problem.'''
    p = args_tuple
    mutated_problem = mutate_problem(p, args.strategy, args.agent)
    return Problem(mutated_problem)

async def main():
    '''Main function to parse arguments, load problems, mutate them, and save results.'''
    parser = argparse.ArgumentParser(description="Problem processor and mutator.")
    parser.add_argument("--strategy", type=str, choices=["rephrase", "expand", "simplify", "add_constraints"],
                        required=True, help="Mutation strategy to apply.")
    parser.add_argument("--num_rounds", type=int, default=3, help="Number of iterations per problem.")
    parser.add_argument("--output", type=str, default="mutated_problems", help="Output file.")
    parser.add_argument("--agent", type=str, default="gpt-4o-mini", help="LLM computing agent.")
    parser.add_argument("--num_problems", type=int, default=2, help="Number of problems to process each round.")
    parser.add_argument("--topk_problems", type=int, default=4, help="Number of top problems to be retained per round.")
    parser.add_argument("--clean_output", type=str, default="yes", choices=["yes", "no"], help="Do you want to clean the output folder for each execution?.")
    
    args = parser.parse_args()

    # Clean generated outputs if specified
    if args.clean_output == "yes":
        clear_ouput()

    # Load problems
    problems = load_problems()
    problems = problems[:args.num_problems]
    leaderboard = Leaderboard(args.topk_problems)

    # Get actual datetime for folder ID
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    mutate_partial = functools.partial(mutate_with_index, args=args)

    # Parallelize mutate problem calls and ensure save_mutations uses await so it doesn't block the program
    for _ in range(args.num_rounds):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            mutated_problems = list(executor.map(mutate_partial, problems))
        await save_mutations(args, mutated_problems, now)        
        await leaderboard.evaluate(problems, args)
        problems = mutated_problems        

if __name__ == "__main__":
    asyncio.run(main())  # Run the main function asynchronously