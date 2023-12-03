# MilkT-RPC

## Architecture

![Architecture](./docs/architecture.png)

<details>
<summary>UML</summary>

```plantuml
@startuml
skinparam componentStyle rectangle

component "Web Server" as web {
    [FastAPI]
    [RpcClient]
    component "Modules" as webmodules {
        [MainEngineAPI] -up-> [FastAPI]: register
        [AlgoWebAPI] -up-> [FastAPI]: register
        [MainEngineAPI] -down-> [RpcClient]
        [AlgoWebAPI] -down-> [RpcClient]
    }
}
HTTP -right-> [FastAPI]
Websocket -right-> [FastAPI]

component "Web Engine" as engine {
    [RpcServer]
    component "MainEngine" as mainengine {
        [RpcServer] -down-> [AlgoRpcServer]
    }
    [RpcServer] -down-> mainengine

    component "AlgoRpcServer" {
        [AlgoEngine]
    }

    [EventEngine] -up-> [RpcServer]: "Put Event"
}

[RpcClient] -down-> [RpcServer]: "RPC"
[RpcServer] -up-> [RpcClient]: "Publish Event"
@enduml
```

</details>
