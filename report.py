import json
import os
import sys
import subprocess

from github import Github

KUROBAKO = os.getenv('KUROBAKO', './kurobako')
OUTPUT_DIR = os.getenv('OUTPUT_DIR', './output/')
ACCESS_TOKEN = os.getenv('GITHUB_TOKEN')


def get_webhook_event():
    filepath = os.getenv('GITHUB_EVENT_PATH')
    with open(filepath, 'r') as f:
        return json.load(f)


def main():
    json_path = sys.argv[1]
    event = get_webhook_event()
    pull_number = event.get('number')
    print("Pull Request:", pull_number)
    repository = event.get('repository').get("full_name")
    print("Repository:", pull_number)

    kurobako_report = subprocess.check_output([
        "sh", "-c", f"cat {json_path} | {KUROBAKO} report",
    ], text=True)

    # TODO(c-bata): Upload to GCS, then add an img tag.
    # subprocess.call([
    #     "sh", "-c", f"cat {json_path} | {KUROBAKO} plot curve -o {OUTPUT_DIR}",
    # ])

    client = Github(ACCESS_TOKEN)
    issue = client.get_repo(repository).get_issue(pull_number)

    # Delete previous comments
    for c in issue.get_comments():
        if c.user.login == 'github-actions[bot]':
            c.delete()

    issue.create_comment(kurobako_report)


if __name__ == '__main__':
    main()
