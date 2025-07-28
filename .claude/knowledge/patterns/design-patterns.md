```mermaid
flowchart LR
    subgraph Creational Patterns
        AbstractFactory
        FactoryMethod
        Builder
        Prototype
        Singleton
    end
    subgraph Structural Patterns
        Adapter
        Bridge
        Composite
        Decorator
        Facade
        Flyweight
        Proxy
    end
    subgraph Behavioral Patterns
        Strategy
        Visitor
        State
        Command
        Observer
        Mediator
        Memento
        TemplateMethod["Template Method"]
        ChainOfResponsibility["Chain of Responsibility"]
        Interpreter
        Iterator
    end
    subgraph Modern Patterns
        DependencyInjection["Dependency Injection"]
        ServiceLocator
        CQRS
        EventSourcing["Event Sourcing"]
        MessageQueue["Message Queue"]
    end
    subgraph Concurrency Patterns
        Reactor
        Proactor
        FuturePromise["Future/Promise"]
        AsyncAwait["Async/Await"]
    end
    subgraph Functional Patterns
        Monad
        Functor
        Currying
        PatternMatching["Pattern Matching"]
        ReactiveStreams["Reactive Streams"]
        Pipeline
    end

    %% Original relationships with labels from image:
    AbstractFactory -->|implement using| FactoryMethod
    AbstractFactory -->|configure factory dynamically| Prototype
    ServiceLocator -->|manages singleton instances| Singleton
    DependencyInjection -->|alternative to| ServiceLocator
    CQRS -->|commands generate events| EventSourcing
    AsyncAwait -->|syntactic sugar for| FuturePromise
    Reactor -->|async variant| Proactor
    Command -->|distributed using| MessageQueue
    Strategy -->|functional equivalent| Functor
    Strategy -->|chained strategies| Pipeline
    Observer -->|async observer| ReactiveStreams
    Pipeline -->|sequential processing| ChainOfResponsibility
    Pipeline -->|transform steps| Decorator

    %% Relationships from the image with their labels:
    Builder -->|creating composites| Composite
    Builder -->|adding mandatories to objects| Iterator
    Iterator -->|enumerating children| Composite
    Iterator -->|saving state of iteration| Memento
    Memento -->|avoiding hysteresis| Command
    Composite -->|composed using| Visitor
    Composite -->|defining traversals| ChainOfResponsibility
    Visitor -->|adding operations| Interpreter
    Flyweight -->|sharing composites| Composite
    Flyweight -->|defining grammar| Interpreter
    Flyweight -->|sharing strategies| State
    Decorator -->|sharing composites| Composite
    Decorator -->|changing skin versus guts| Strategy
    Strategy -->|sharing strategies| Flyweight
    State -->|sharing states| Flyweight
    State -->|sharing terminal symbols| Interpreter
    Mediator -->|complex dependency management| Observer
    TemplateMethod -->|often uses| FactoryMethod
    Prototype -->|implement using| AbstractFactory
    Facade -->|single instance| Singleton
    Singleton -->|single instance| AbstractFactory
    Proxy -->|adapting interface| Adapter
    Bridge -->|multiple adapters| Adapter
    Command -->|macro commands| Composite

    %% Additional inferred relationships with descriptors:
    Observer -->|broadcasts to| Mediator
    Iterator -->|traversal for| Visitor
    Command -->|undo/redo using| Memento
    Decorator -->|protection/caching| Proxy
    ChainOfResponsibility -->|delegates to| Command
    TemplateMethod -->|pluggable algorithm| Strategy
    FactoryMethod -->|creates products for| Builder
    Adapter -->|simplifies using| Facade
    Observer -->|persisted as| EventSourcing
    Mediator -->|coordinates via| MessageQueue
    Proxy -->|unified interface| Facade
    Strategy -->|algorithm skeleton| TemplateMethod
    Visitor -->|type-based dispatch| Strategy
    State -->|state-specific| Strategy
    CQRS -->|command side uses| Command
    ReactiveStreams -->|event streams for| EventSourcing
    Monad -->|computation context for| FuturePromise
    PatternMatching -->|functional visitor| Visitor
    Currying -->|partial construction| Builder
    Pipeline -->|stream processing| ReactiveStreams
    Builder -->|clone and modify| Prototype
    Facade -->|simplifies| Bridge
    Composite -->|tree grammar| Interpreter
    DependencyInjection -->|constructs using| Builder
    DependencyInjection -->|creates via| AbstractFactory
    EventSourcing -->|event snapshots| Memento
    MessageQueue -->|delivers events for| EventSourcing
    FuturePromise -->|async values in| ReactiveStreams
    Functor -->|specialized| Monad
    PatternMatching -->|dispatch mechanism| Strategy
    Iterator -->|push-based| ReactiveStreams
    ```