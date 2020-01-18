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


def get_kurobako_image_path():
    # TODO(c-bata): specify output filename in the option at kurobako plot curve command.
    # It seems kurobako accepts multiple studies, so it seems to need more discussions.
    for filepath in os.listdir(OUTPUT_DIR):
        if filepath.endswith('.png'):
            return os.path.join(OUTPUT_DIR, filepath)
    raise Exception('kurobako image not found.')


def main():
    print(sys.argv)
    json_path = sys.argv[1]
    public_image_url = sys.argv[2] if len(sys.argv) > 2 else ''

    event = get_webhook_event()
    pull_number = event.get('number')
    print("Pull Request:", pull_number)
    repository = event.get('repository').get("full_name")
    print("Repository:", pull_number)

    # Plot curve
    subprocess.run([
        "sh", "-c", f"cat {json_path} | {KUROBAKO} plot curve -o {OUTPUT_DIR}",
    ], check=True)
    print(f"::set-output name=image-path::{get_kurobako_image_path()}")

    # Generate markdown report
    kurobako_report = subprocess.check_output([
        "sh", "-c", f"cat {json_path} | {KUROBAKO} report",
    ], text=True)

    client = Github(ACCESS_TOKEN)
    issue = client.get_repo(repository).get_issue(pull_number)

    body = f"""
# Kurobako

{f'![plot curve image]({public_image_url})' if public_image_url else ''}

<details>
{kurobako_report}
</details>
"""[1:]

    # Comment to the pull request or edit if previous comment exists.
    for c in issue.get_comments():
        if c.user.login == 'github-actions[bot]':
            c.edit(body)
            break
    else:
        issue.create_comment(body)


if __name__ == '__main__':
    main()
