#!/usr/bin/env python3
import subprocess
import json
import matplotlib.pyplot as plt

def run_gh_command(command):
    """
    Run a GitHub CLI command and return its trimmed stdout.
    Raises an exception if the command fails.
    """
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def get_repo_names(username):
    """
    Returns a list of repository names for the given username that are NOT forks.
    """
    cmd = [
        "gh", "repo", "list", username,
        "--json", "name,isFork",
        "-q", '.[] | select(.isFork == false) | .name'
    ]
    output = run_gh_command(cmd)
    # Split the output into lines; each line is a repository name.
    repos = output.splitlines()
    return repos

def get_traffic_data(username, repo):
    """
    Uses the GitHub CLI to fetch the clones traffic data for a repository.
    Returns the parsed JSON data or None if not available.
    """
    cmd = [
        "gh", "api", f"repos/{username}/{repo}/traffic/clones",
        "--jq", "."
    ]
    try:
        output = run_gh_command(cmd)
        if output.lower() == "null" or output == "":
            return None
        data = json.loads(output)
        return data
    except subprocess.CalledProcessError as e:
        print(f"Error fetching traffic data for {repo}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decode error for {repo}: {e}")
        return None

def main():
    # Prompt for GitHub username.
    username = input("Enter GitHub username: ").strip()
    print(f"Fetching repository list for {username} ...")
    repos = get_repo_names(username)
    print(f"Found {len(repos)} repositories (non-forks).")
    
    all_data = []
    for repo in repos:
        print(f"Fetching traffic data for {repo} ...")
        traffic = get_traffic_data(username, repo)
        # If no traffic data is returned, use zeros.
        if traffic is None:
            traffic = {"count": 0, "uniques": 0, "clones": []}
        all_data.append({"name": repo, "traffic": traffic})
    
    # Optionally save the gathered data to a JSON file.
    with open("all_traffic_report.json", "w") as f:
        json.dump(all_data, f, indent=4)
    print("Traffic data saved to all_traffic_report.json")
    
    # Prepare data for visualization.
    repo_names = []
    total_clones = []
    unique_clones = []
    
    for item in all_data:
        repo_names.append(item["name"])
        total_clones.append(item["traffic"].get("count", 0))
        unique_clones.append(item["traffic"].get("uniques", 0))
    
    # Sort the repositories by total clones in descending order.
    sorted_data = sorted(zip(total_clones, unique_clones, repo_names), reverse=True)
    if sorted_data:
        sorted_total, sorted_unique, sorted_names = zip(*sorted_data)
    else:
        print("No data available to visualize.")
        return

    # Determine how many items to display (top 20 or less).
    top_n = min(20, len(sorted_names))
    indices = list(range(top_n))
    bar_width = 0.35

    # Create a horizontal bar chart comparing Total and Unique clones.
    plt.figure(figsize=(12, 8))
    plt.barh(indices, sorted_total[:top_n], bar_width, label="Total Clones")
    plt.barh([i + bar_width for i in indices], sorted_unique[:top_n], bar_width, label="Unique Clones")
    plt.xlabel("Number of Clones")
    plt.ylabel("Repository")
    plt.title("GitHub Repo Traffic: Total vs Unique Clones (Top Repositories)")
    plt.yticks([i + bar_width/2 for i in indices], sorted_names[:top_n])
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    print("Visualization complete. Enjoy your chart!")

if __name__ == "__main__":
    main()

