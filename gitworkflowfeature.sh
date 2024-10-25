#Git Workflow for Feature Integration
# Create a new directory for your project
mkdir my-project
cd my-project

# Initialize a new git repository
git init

# Create a README file
echo "# My Project" >> README.md

# Add and commit the README file
git add README.md
git commit -m "Initial commit"
# Create and switch to the develop branch
git checkout -b develop
# Create a new feature branch (e.g., feature/login)
git checkout -b feature/login
# Make changes to your project files (e.g., adding a login feature)
echo "Adding login feature" >> login.py

# Add and commit changes
git add login.py
git commit -m "Implement login feature"

# Switch back to develop branch
git checkout develop

# Pull the latest changes from develop
git pull origin develop

# Switch back to your feature branch
git checkout feature/login

# Rebase or merge the changes from develop into your feature branch
git rebase develop
# OR
# git merge develop

git add <resolved-file>
git rebase --continue
# Switch to develop branch
git checkout develop

# Merge the feature branch
git merge feature/login
# Push changes to the remote develop branch
git push origin develop
# Delete the local feature branch
git branch -d feature/login

# If necessary, delete the remote feature branch
git push origin --delete feature/login

#release new feature
git checkout main
git merge develop
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin main
git push origin --tags

