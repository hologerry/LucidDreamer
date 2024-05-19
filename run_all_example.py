import argparse
import os
import subprocess
import time

import yaml


# Function to read a YAML file
def read_yaml(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


# Example usage
file_path = "examples.yaml"
yaml_data = read_yaml(file_path)
print(len(yaml_data))


def execute_command(command):
    start_time = time.time()
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    end_time = time.time()
    execution_time = end_time - start_time

    return process.stdout, process.stderr, execution_time


parser = argparse.ArgumentParser(description="Arguments for LucidDreamer")
# Input options
parser.add_argument("-i", type=int, default=0)
parser.add_argument("-p", type=int, default=1)
args = parser.parse_args()

cur_data = yaml_data[args.i :: args.p]

for one_example in cur_data:
    img_path = one_example["image_filepath"].replace("examples/", "")
    # style_prompt = one_example["style_prompt"]
    content_prompt = one_example["content_prompt"]
    # negation_prompt = one_example['negation_prompt']
    # background_prompt = one_example['background']
    if not os.path.exists(img_path):
        print(f"Image not found: {img_path}")
        continue
    cmd = f"python run.py -img {img_path} -t '{content_prompt}'"
    print(cmd)
    # Execute the command
    # os.system(cmd)
    stdout, stderr, execution_time = execute_command(cmd)
    base_name = os.path.basename(img_path).replace(".png", "")
    with open(f"outputs/{base_name}_stdout.txt", "w") as file:
        file.write(stdout)
    with open(f"outputs/{base_name}_stderr.txt", "w") as file:
        file.write(stderr)
    with open(f"outputs/{base_name}_time.txt", "w") as file:
        file.write(f"{img_path}\n")
        file.write(f"Execution Time: {execution_time} seconds\n")
    print(execution_time)
