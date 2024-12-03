# GitHub Conversation Starter - Mermaid Architecture

```mermaid
graph TD
    subgraph Frontend
        A[index.html] --> |"HTTP"| B["Flask App"]
        A --> |"Display"| D["Profile Display"]
        A --> |"Display"| E["Contribution Stats"]
        A --> |"Display"| F["Conversation Starters"]
        A --> |"Input"| C["GitHub Username Input"]
    end

    subgraph "Flask Backend"
        B --> |"Routes"| G["Home Route"]
        B --> |"Routes"| H["Analyze Route"]
        H --> |"Process"| I["GitHub Integration"]
    end

    subgraph "GitHub Integration"
        I --> |"API Calls"| J["GitHub API"]
        J --> |"Data"| K["Profile Data"]
        J --> |"Data"| L["Contrib Data"]
        I --> |"Generate"| M["Conversation Starters"]
    end

    subgraph "External Services"
        J --> |"Auth"| N["GitHub Token"]
        M --> |"API"| O["OpenAI API"]
    end

    subgraph Configuration
        P["Environment Variables"] --> |"Config"| B
        P --> |"Auth"| N
        P --> |"Auth"| O
    end
```
