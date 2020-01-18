import json
import os
import sys

from github import Github

ACCESS_TOKEN = os.getenv('GITHUB_TOKEN')


def get_webhook_event():
    filepath = os.getenv('GITHUB_EVENT_PATH')
    with open(filepath, 'r') as f:
        return json.load(f)


def generate_report(kurobako_report, public_image_url):
    header_trimmed = kurobako_report[len('# Benchmark Result Report\n\n'):]
    metadata, detail = header_trimmed.split('## Table of Contents\n')[:2]
    body = f"""
# Kurobako Benchmark

![plot curve image]({public_image_url})

{metadata}

<details>
<summary>See details of benchmark results</summary>

## Table of Contents
{detail}

</details>
"""[1:]
    return body


def main():
    print(sys.argv)
    markdown_report_path = sys.argv[1]
    public_image_url = sys.argv[2]

    event = get_webhook_event()
    pull_number = event.get('number')
    print("Pull Request:", pull_number)

    repository = event.get('repository').get("full_name")
    print("Repository:", pull_number)

    with open(markdown_report_path, 'r') as f:
        kurobako_report = "\n".join(f.readlines())

    client = Github(ACCESS_TOKEN)
    issue = client.get_repo(repository).get_issue(pull_number)
    body = generate_report(kurobako_report, public_image_url)

    # Comment to the pull request or edit if previous comment exists.
    for c in issue.get_comments():
        if not c.user.login.startswith('github-actions'):
            continue
        if not c.body.startswith('# Kurobako Benchmark'):
            continue

        c.edit(body)
        break
    else:
        issue.create_comment(body)


if __name__ == '__main__':
    main()
