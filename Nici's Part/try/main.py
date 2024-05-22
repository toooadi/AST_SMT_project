import subprocess
import z3

def run_janus_command():
    command = [
        'py', '../janus/bin/janus', 'z3',
        '--rule-set', 'operator-replacement',
        '-o', 'sat',
        '../examples/phi1.smt2'
    ]
    
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Command output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred while running the command:", e.stderr)

if __name__ == "__main__":
    run_janus_command()