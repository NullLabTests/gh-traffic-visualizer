repo-traffic-visualizer
Overview
repo-traffic-visualizer is a Python tool that allows you to track and visualize GitHub traffic data for your repositories. By utilizing the GitHub API, it gathers clone and unique clone statistics for each of your repositories and presents the data in an easy-to-understand bar chart format.

The tool is designed to help GitHub repository owners analyze the traffic patterns and understand the engagement with their repositories. It’s especially useful for users who want to track their own repositories' traffic and see how their code is being accessed over time.

Features
Fetches GitHub traffic data including total clones and unique clones.
Provides an intuitive bar chart visualization of the data.
Allows you to specify a GitHub username to gather data from all non-forked repositories.
Saves the traffic data in JSON format for further analysis.
Simple one-command setup for ease of use.
Installation
Clone this repository:

bash
Copy
Edit
git clone https://github.com/NullLabTests/repo-traffic-visualizer.git
cd repo-traffic-visualizer
Install the required dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Usage
Make sure you have authenticated with the GitHub API using gh CLI or a personal access token.

Run the following command to start the data collection and visualization process:

bash
Copy
Edit
python3 rtv.py
You will be prompted to enter your GitHub username. The script will fetch traffic data for all your repositories and generate visualizations.

Example Output
kotlin
Copy
Edit
Enter GitHub username: NullLabTests
Fetching repository list for NullLabTests ...
Found 10 repositories (non-forks).
Fetching traffic data for ArXivEvolution ...
Fetching traffic data for SelfImprovingAgent ...
Fetching traffic data for VivaCell ...
...
Traffic data saved to all_traffic_report.json
Matplotlib will display a bar chart of the clone statistics for your repositories.

License
This project is licensed under the BSD-3 License - see the LICENSE file for details.


