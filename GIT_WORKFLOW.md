# Git Workflow Documentation

This document provides detailed visual guides for working with git in the Abacus Chat Exporter project.

## 📚 Table of Contents

- [Repository Structure](#repository-structure)
- [Development Workflow](#development-workflow)
- [Branching Strategy](#branching-strategy)
- [Feature Development Lifecycle](#feature-development-lifecycle)
- [Collaboration Patterns](#collaboration-patterns)
- [Advanced Git Operations](#advanced-git-operations)

## 🏗️ Repository Structure

### Repository Overview

```mermaid
graph TB
    subgraph "Remote Repository (GitHub)"
        R[origin/main]
        R1[origin/feature/*]
        R2[origin/claude/*]
    end

    subgraph "Local Repository"
        L[local/main]
        L1[feature/new-feature]
        L2[bugfix/issue-123]
    end

    subgraph "Working Directory"
        W[Modified Files]
        S[Staged Changes]
    end

    R -->|git clone| L
    R -->|git fetch| L
    L -->|git checkout -b| L1
    L -->|git checkout -b| L2
    W -->|git add| S
    S -->|git commit| L1
    L1 -->|git push| R1
```

### Branch Hierarchy

```mermaid
graph TD
    A[main] --> B[Long-lived Branches]
    A --> C[Short-lived Branches]

    B --> B1[main - Production ready code]
    B --> B2[develop - Integration branch for features]

    C --> C1[feature/* - New features]
    C --> C2[bugfix/* - Bug fixes]
    C --> C3[hotfix/* - Critical fixes]
    C --> C4[docs/* - Documentation]
    C --> C5[refactor/* - Code improvements]
    C --> C6[claude/* - AI-assisted development]

    style B1 fill:#4CAF50
    style B2 fill:#2196F3
    style C1 fill:#FF9800
    style C2 fill:#F44336
    style C3 fill:#9C27B0
    style C4 fill:#00BCD4
    style C5 fill:#FFEB3B
    style C6 fill:#E91E63
```

## 🔄 Development Workflow

### Complete Development Cycle

```mermaid
sequenceDiagram
    actor Dev as Developer
    participant WD as Working Directory
    participant Staging as Staging Area
    participant Local as Local Repo
    participant Remote as Remote Repo
    participant CI as CI/CD
    participant Rev as Reviewers

    Dev->>WD: Make changes
    Dev->>WD: Test locally
    Dev->>Staging: git add
    Dev->>Local: git commit -m "message"
    Dev->>Local: Run pre-commit hooks

    alt Pre-commit passes
        Dev->>Remote: git push origin branch
        Remote->>CI: Trigger pipeline
        CI->>CI: Run tests
        CI->>CI: Run linters
        CI->>CI: Build project

        alt CI passes
            CI-->>Remote: ✅ Success
            Dev->>Remote: Create Pull Request
            Remote->>Rev: Request review
            Rev->>Remote: Approve PR
            Remote->>Remote: Merge to main
        else CI fails
            CI-->>Remote: ❌ Failed
            Dev->>WD: Fix issues
        end
    else Pre-commit fails
        Local-->>Dev: ❌ Hook failed
        Dev->>WD: Fix issues
    end
```

### Daily Development Flow

```mermaid
flowchart TD
    Start([Start Day]) --> Pull[Pull latest changes]
    Pull --> Branch{Need new<br/>branch?}

    Branch -->|Yes| Create[Create feature branch]
    Branch -->|No| Checkout[Checkout existing branch]

    Create --> Code[Write code]
    Checkout --> Code

    Code --> Test[Run tests]
    Test --> TestPass{Tests pass?}

    TestPass -->|No| Debug[Debug issues]
    Debug --> Code

    TestPass -->|Yes| Stage[Stage changes]
    Stage --> Commit[Commit with message]
    Commit --> Push[Push to remote]

    Push --> PR{Ready for<br/>PR?}
    PR -->|No| More{More work?}
    More -->|Yes| Code
    More -->|No| End([End Day])

    PR -->|Yes| CreatePR[Create Pull Request]
    CreatePR --> Review[Request review]
    Review --> End
```

## 🌿 Branching Strategy

### Feature Branch Workflow

```mermaid
gitGraph
    commit id: "Initial"
    commit id: "Setup project"

    branch feature/export-tool
    checkout feature/export-tool
    commit id: "Add API client"
    commit id: "Implement export logic"
    commit id: "Add tests"

    checkout main
    branch feature/pdf-processor
    checkout feature/pdf-processor
    commit id: "Add PDF upload"
    commit id: "Add processing logic"

    checkout main
    merge feature/export-tool tag: "v0.1.0"
    commit id: "Release v0.1.0"

    checkout feature/pdf-processor
    commit id: "Add multi-prompt support"

    checkout main
    merge feature/pdf-processor tag: "v0.2.0"
    commit id: "Release v0.2.0"
```

### Hotfix Workflow

```mermaid
gitGraph
    commit id: "v1.0.0" tag: "v1.0.0"
    commit id: "Feature work"

    branch hotfix/critical-bug
    checkout hotfix/critical-bug
    commit id: "Fix critical bug"
    commit id: "Add regression test"

    checkout main
    merge hotfix/critical-bug tag: "v1.0.1"

    branch develop
    checkout develop
    merge hotfix/critical-bug
    commit id: "Continue development"
```

### Multi-Feature Development

```mermaid
gitGraph
    commit id: "base"

    branch feature/A
    branch feature/B
    branch feature/C

    checkout feature/A
    commit id: "A1"
    commit id: "A2"

    checkout feature/B
    commit id: "B1"
    commit id: "B2"

    checkout feature/C
    commit id: "C1"

    checkout main
    merge feature/A

    checkout feature/B
    commit id: "B3"

    checkout main
    merge feature/B

    checkout feature/C
    commit id: "C2"
    commit id: "C3"

    checkout main
    merge feature/C
```

## 🔄 Feature Development Lifecycle

### From Idea to Production

```mermaid
stateDiagram-v2
    [*] --> Planning: New feature idea
    Planning --> BranchCreated: Create feature branch
    BranchCreated --> Development: Start coding
    Development --> Testing: Code complete
    Testing --> CodeReview: Tests pass
    CodeReview --> ChangesRequested: Issues found
    ChangesRequested --> Development: Fix issues
    CodeReview --> Approved: Review approved
    Approved --> Staging: Merge to staging
    Staging --> Production: Deploy to production
    Production --> [*]: Feature live
```

### Detailed Feature Flow

```mermaid
flowchart TD
    A[Issue Created] --> B[Assign to Developer]
    B --> C[Create Feature Branch]
    C --> D[Implement Feature]
    D --> E[Write Tests]
    E --> F[Run Tests Locally]

    F --> G{Tests Pass?}
    G -->|No| H[Fix Bugs]
    H --> F

    G -->|Yes| I[Commit Changes]
    I --> J[Push to Remote]
    J --> K[Create Pull Request]

    K --> L[Automated Checks]
    L --> M{Checks Pass?}
    M -->|No| N[Fix Issues]
    N --> J

    M -->|Yes| O[Request Code Review]
    O --> P[Code Review]

    P --> Q{Approved?}
    Q -->|No| R[Address Feedback]
    R --> J

    Q -->|Yes| S[Merge to Main]
    S --> T[Delete Feature Branch]
    T --> U[Deploy to Production]
    U --> V[Close Issue]
```

## 🤝 Collaboration Patterns

### Fork-Based Collaboration

```mermaid
sequenceDiagram
    participant U as Upstream (danindiana/abacus-chat-exporter)
    participant F as Your Fork
    participant L as Local Repo

    Note over U,L: Initial Setup
    U->>F: Fork repository
    F->>L: git clone

    Note over U,L: Keep Fork Updated
    U->>L: git fetch upstream
    L->>L: git merge upstream/main
    L->>F: git push origin main

    Note over U,L: Contribute Changes
    L->>L: git checkout -b feature/my-feature
    L->>L: Make changes & commit
    L->>F: git push origin feature/my-feature
    F->>U: Create Pull Request
    U->>U: Review & Merge
```

### Team Collaboration Workflow

```mermaid
sequenceDiagram
    participant A as Developer A
    participant B as Developer B
    participant R as Repository
    participant M as Maintainer

    A->>R: Push feature/A
    B->>R: Push feature/B

    A->>R: Create PR for feature/A
    M->>R: Review PR
    M->>R: Request changes

    A->>R: Push updates
    M->>R: Approve & Merge

    B->>B: Rebase on latest main
    B->>R: Push feature/B (updated)
    B->>R: Create PR for feature/B
    M->>R: Review & Merge
```

### Conflict Resolution

```mermaid
flowchart TD
    A[Pull latest main] --> B[Merge/Rebase main into feature]
    B --> C{Conflicts?}

    C -->|No| D[Continue development]

    C -->|Yes| E[Open conflicted files]
    E --> F[Review conflict markers]
    F --> G[Choose correct version]
    G --> H[Remove conflict markers]
    H --> I[Test resolved code]

    I --> J{Works correctly?}
    J -->|No| K[Fix issues]
    K --> I

    J -->|Yes| L[Stage resolved files]
    L --> M[Commit merge/rebase]
    M --> D
```

## 🎯 Advanced Git Operations

### Interactive Rebase Workflow

```mermaid
stateDiagram-v2
    [*] --> StartRebase: git rebase -i HEAD~5
    StartRebase --> ChooseAction: Select commits

    state ChooseAction {
        [*] --> Pick: Keep commit as-is
        [*] --> Squash: Combine with previous
        [*] --> Edit: Modify commit
        [*] --> Drop: Remove commit
    }

    ChooseAction --> ApplyChanges: Save rebase plan
    ApplyChanges --> ResolveConflicts
    ResolveConflicts --> [*]: Complete rebase
```

### Git Stash Workflow

```mermaid
flowchart LR
    A[Working on feature] --> B{Need to switch<br/>branches?}
    B -->|Yes| C[git stash]
    B -->|No| A

    C --> D[Switch branches]
    D --> E[Do urgent work]
    E --> F[git commit]
    F --> G[Switch back to feature]
    G --> H[git stash pop]
    H --> I[Continue work]
```

### Cherry-Pick Process

```mermaid
gitGraph
    commit id: "A"
    commit id: "B"

    branch feature-1
    commit id: "C"
    commit id: "D (bug fix)" type: HIGHLIGHT
    commit id: "E"

    checkout main
    cherry-pick id: "D (bug fix)"
    commit id: "D' (cherry-picked)"

    branch feature-2
    commit id: "F"
    cherry-pick id: "D (bug fix)"
    commit id: "D'' (cherry-picked)"
```

### Bisect for Bug Hunting

```mermaid
flowchart TD
    A[Bug discovered] --> B[git bisect start]
    B --> C[git bisect bad - mark current commit]
    C --> D[git bisect good <hash> - mark known good commit]

    D --> E[Git checks out middle commit]
    E --> F[Test for bug]

    F --> G{Bug present?}
    G -->|Yes| H[git bisect bad]
    G -->|No| I[git bisect good]

    H --> J{More commits<br/>to check?}
    I --> J

    J -->|Yes| E
    J -->|No| K[Git identifies first bad commit]
    K --> L[git bisect reset]
    L --> M[Fix the bug]
```

## 🔀 Merge Strategies

### Fast-Forward Merge

```mermaid
gitGraph
    commit id: "A"
    commit id: "B"

    branch feature
    commit id: "C"
    commit id: "D"

    checkout main
    merge feature tag: "FF Merge"
```

### Three-Way Merge

```mermaid
gitGraph
    commit id: "A"
    commit id: "B"

    branch feature
    commit id: "C"
    commit id: "D"

    checkout main
    commit id: "E"

    merge feature tag: "Merge Commit"
```

### Rebase and Merge

```mermaid
gitGraph
    commit id: "A"
    commit id: "B"

    branch feature
    commit id: "C"
    commit id: "D"

    checkout main
    commit id: "E"

    checkout feature
    commit id: "C' (rebased)" type: HIGHLIGHT
    commit id: "D' (rebased)" type: HIGHLIGHT

    checkout main
    merge feature tag: "FF after rebase"
```

## 🔐 Tag and Release Workflow

### Semantic Versioning Tags

```mermaid
gitGraph
    commit id: "Initial" tag: "v0.1.0"
    commit id: "Add features"
    commit id: "More features" tag: "v0.2.0"

    branch bugfix
    commit id: "Fix bug"
    checkout main
    merge bugfix tag: "v0.2.1"

    commit id: "Breaking change"
    commit id: "Update API" tag: "v1.0.0"

    commit id: "New feature"
    commit id: "Another feature" tag: "v1.1.0"
```

### Release Process

```mermaid
flowchart TD
    A[Feature complete] --> B[Create release branch]
    B --> C[Update version numbers]
    C --> D[Update CHANGELOG]
    D --> E[Create release commit]
    E --> F[Tag release]

    F --> G[Merge to main]
    G --> H[Deploy to production]
    H --> I[Create GitHub release]

    I --> J[Generate release notes]
    J --> K[Publish release]
    K --> L[Merge back to develop]
```

## 📊 Git History Visualization

### Understanding Git Log

```mermaid
graph LR
    A[HEAD] --> B[main]
    B --> C[commit C]
    C --> D[commit B]
    D --> E[commit A]

    F[feature/new] --> G[commit F]
    G --> H[commit E]
    H --> D

    style A fill:#ff6b6b
    style B fill:#4ecdc4
    style F fill:#95e1d3
```

### Commit Graph with Multiple Branches

```mermaid
gitGraph
    commit id: "1"
    commit id: "2"

    branch develop
    checkout develop
    commit id: "3"

    branch feature/A
    checkout feature/A
    commit id: "4"
    commit id: "5"

    checkout develop
    branch feature/B
    commit id: "6"

    checkout develop
    merge feature/A
    commit id: "7"

    checkout feature/B
    commit id: "8"

    checkout develop
    merge feature/B

    checkout main
    merge develop tag: "v1.0.0"
```

## 🛠️ Git Commands Reference

### Common Workflow Commands

```mermaid
graph TD
    A[Start] --> B{What do you<br/>want to do?}

    B -->|Create branch| C[git checkout -b name]
    B -->|Switch branch| D[git checkout name]
    B -->|View changes| E[git status / git diff]
    B -->|Stage changes| F[git add]
    B -->|Commit| G[git commit -m message]
    B -->|Push| H[git push origin branch]
    B -->|Pull updates| I[git pull origin branch]
    B -->|View history| J[git log]
    B -->|Stash changes| K[git stash]
    B -->|Merge branch| L[git merge branch]
    B -->|Rebase| M[git rebase branch]
    B -->|Tag release| N[git tag -a v1.0.0]
```

## 🎓 Best Practices

### Commit Frequency

```mermaid
timeline
    title Good Commit Practice
    section Monday
        Morning : Implement feature skeleton
        Noon : Add core functionality
        Afternoon : Add error handling
        Evening : Add tests
    section Tuesday
        Morning : Fix test failures
        Noon : Refactor code
        Afternoon : Update documentation
        Evening : Final polish
```

### Branch Lifecycle

```mermaid
gantt
    title Feature Branch Lifecycle
    dateFormat YYYY-MM-DD
    section Planning
        Create issue           :a1, 2025-01-01, 1d
    section Development
        Create branch         :a2, after a1, 1d
        Implement feature     :a3, after a2, 5d
        Write tests          :a4, after a3, 2d
    section Review
        Create PR            :a5, after a4, 1d
        Code review          :a6, after a5, 2d
        Address feedback     :a7, after a6, 1d
    section Deployment
        Merge to main        :a8, after a7, 1d
        Deploy               :a9, after a8, 1d
        Delete branch        :a10, after a9, 1d
```

## 📚 Additional Resources

- [Git Official Documentation](https://git-scm.com/doc)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

---

**Note**: These diagrams and workflows are designed to provide visual guidance. Adapt them to fit your specific workflow and team needs.
