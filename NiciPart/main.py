import os
import subprocess


def run_janus_command():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    janus_path = os.path.join(script_dir, 'janus', 'bin', 'janus')
    example_path = os.path.join(script_dir, 'janus', 'examples', 'phi1.smt2')
    print("Janus path:", janus_path)
    print("Example path:", example_path)

    command = [
        'py', janus_path, 'z3',
        '--rule-set', 'operator-replacement',
        '-o', 'sat',
        example_path
    ]
    
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Command output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the command:", e.stderr)

if __name__ == "__main__":
    run_janus_command()
