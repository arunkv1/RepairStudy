import requests

# Replace with your personal access token

GITHUB_TOKEN = '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'
headers = {'Authorization': f'token {GITHUB_TOKEN}'}
# Define search parameters
query = (
    "accessibility in:issues "
    "stars:>1 "
    # "pushed:>2015-01-01 "  # Uncomment for pushed date filter
    # "forks:>10 "  # Uncomment for minimum forks filter
)
url = 'https://api.github.com/search/issues'
all_issues = []
page = 1

# Loop to paginate through results
while True:
    # Add pagination parameters to the URL
    paginated_url = f"{url}?q={query}&per_page=100&page={page}"
    response = requests.get(paginated_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch issues: {response.status_code}")
        break
    
    # Parse response and add to list
    issues = response.json().get('items', [])
    if not issues:
        break  # Stop if no more results
    
    all_issues.extend(issues)
    page += 1  # Move to the next page
    
    # Optional: stop if reaching GitHub’s limit
    if len(all_issues) >= 1000:
        print("Reached GitHub's 1,000 result cap.")
        break

# Print a summary of results
for issue in all_issues:
    print(f"Issue Title: {issue['title']}")
    print(f"Repository URL: {issue['repository_url']}")
    
    # Optional: fetch repository name if desired
    repo_response = requests.get(issue['repository_url'], headers=headers)
    if repo_response.status_code == 200:
        repo_data = repo_response.json()
        print(f"Repository Name: {repo_data.get('full_name')}")
    
    print(f"Issue URL: {issue['html_url']}")
    print(f"Description: {issue['body'][:200]}...")  # Display first 200 chars
    print("=" * 80)

print(f"Total issues found: {len(all_issues)}")
