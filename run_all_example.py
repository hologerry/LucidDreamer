import argparse
import os
import subprocess
import time

from argparse import ArgumentParser
from multiprocessing import Pool

import torch
import yaml


def execute_command(cmd_p):
    command, base_name = cmd_p
    start_time = time.time()
    os.system(command)
    end_time = time.time()
    execution_time = end_time - start_time
    # stdout = process.stdout
    # stderr = process.stderr

    # with open(f"outputs/{base_name}_stdout.txt", "w") as file:
    #     file.write(stdout)
    # with open(f"outputs/{base_name}_stderr.txt", "w") as file:
    #     file.write(stderr)
    with open(f"outputs/{base_name}_time.txt", "w") as file:
        file.write(f"{base_name}\n")
        file.write(f"Execution Time: {execution_time} seconds\n")


# Function to read a YAML file
def read_yaml(file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def main_process(yaml_data, process_num):
    available_cuda = torch.cuda.device_count()
    print(f"Available CUDA: {available_cuda}")
    cmds = []
    cuda_idx = 0
    for one_example in yaml_data:
        img_path = one_example["image_filepath"].replace("examples/", "")
        if not os.path.exists(img_path):
            print(f"Image not found: {img_path}")
            continue
        content_prompt = one_example["content_prompt"]
        base_name = os.path.basename(img_path).replace(".png", "")
        if not os.path.exists(img_path):
            print(f"Image not found: {img_path}")
            return
        if os.path.exists(f"outputs/{base_name}_time.txt"):
            print(f"Already processed: {base_name}")
            continue
        cmd = f"export CUDA_VISIBLE_DEVICES={cuda_idx%available_cuda} && python run.py -img {img_path} -t '{content_prompt}'"
        cuda_idx += 1
        cmds.append((cmd, base_name))

    pool = Pool(process_num)
    pool.map(execute_command, cmds)
    pool.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-j", type=int, default=4)

    args = parser.parse_args()

    # Example usage
    file_path = "examples.yaml"
    yaml_data = read_yaml(file_path)
    print(len(yaml_data))

    main_process(yaml_data, args.j)
