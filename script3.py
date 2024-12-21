import subprocess
import os

# Define the paths to the two repository directories
REPO1_DIR = os.path.join(os.path.dirname(__file__), "repo1/test_project_2")
# REPO2_DIR = os.path.join(os.path.dirname(__file__), "repo2/test_project_2")
REMOTE_NAME = "origin"  
BRANCH_NAME = "main" 

def run_command(command, cwd=None):
    """Run a command and return the output."""
    result = subprocess.run(command, shell=True, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Command failed with error code {result.returncode}")
        print(f"Command: {command}")
        print(f"Output: {result.stdout}")
        print(f"Error: {result.stderr}")
        raise subprocess.CalledProcessError(result.returncode, command)
    return result.stdout

def merge_and_push(repo_dir):
    """Merge changes and push to the remote repository."""
    print(f"Processing repository in {repo_dir}...")

    os.chdir(repo_dir)
    
    run_command(f"git fetch {REMOTE_NAME}")
    run_command(f"git checkout {BRANCH_NAME}")

    # Pull the latest changes from the remote branch
    try:
        run_command(f"git pull {REMOTE_NAME} {BRANCH_NAME}")
    except subprocess.CalledProcessError:
        print("Pull conflicts detected. Opening merge tool...")
        # Resolve conflicts using mergetool
        run_command("git mergetool")
        print("Committing resolved changes...")
        run_command('git commit -am "Resolved merge conflicts"')

    # Push changes to the remote
    print("Pushing changes to remote...")
    run_command(f"git push {REMOTE_NAME} {BRANCH_NAME}")

def main():
    try:
        merge_and_push(REPO1_DIR)
        # merge_and_push(REPO2_DIR)
        print("Script completed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
