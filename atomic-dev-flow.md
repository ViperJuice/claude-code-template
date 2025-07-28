```mermaid
flowchart TD
    %% ─────────────────────────────────────────────────────
    %% 1. Ingestion / Design sources
    %% ─────────────────────────────────────────────────────
    subgraph "Codebase Discovery & Design"
        Cartographer["Codebase Cartographer"]
        CodebaseArchitect["Codebase Architect"]
    end

    %% ─────────────────────────────────────────────────────
    %% 2. Common output artefact
    %% ─────────────────────────────────────────────────────
    Roadmap["roadmap.md (C4 diagrams + Phase Info)"]

    Cartographer -- "Extract C4 model from existing codebase" --> CodebaseArchitect
    CodebaseArchitect -- "Generate roadmap with C4 diagrams + Phase Info" --> Roadmap

    %% ─────────────────────────────────────────────────────
    %% 3. Phase & C4 structure inside roadmap.md
    %% ─────────────────────────────────────────────────────
    Roadmap[("C1: Context description languages + Phased to-do list")]

    %% ─────────────────────────────────────────────────────
    %% 4. Hand‑off for each phase
    %% ─────────────────────────────────────────────────────
    RoadmapToContainerConverter["Roadmap to Container Converter"]
    RoadmapToContainerConverter -- "Container definitions" --> EntityAnalyst["Renovation Architect [B0L0]"]
    Roadmap -- "roadmap information" --> RoadmapToContainerConverter
    EntityAnalyst -- "Branch 0 implementation summary" --> ImplementationSummarizer["Implementation Summarizer B0"]
    ImplementationSummarizer -- "roadmap update" --> Roadmap
    
    %% ─────────────────────────────────────────────────────
    %% BRANCH 0 - Parallel Flow
    %% ─────────────────────────────────────────────────────
    subgraph "Branch 0 Flow"
        EntityAnalyst -- "[B0] Proposed interfaces + test analyses" --> RenovationTesterBranch0["Renovation Interface Test Prototyper [B0L0]"]
        
        RenovationTesterBranch0 -- "Validated tests" --> TestBank0[("Renovation Test Bank [B0L0]")]
        RenovationTesterBranch0 -- "New Validated Interfaces" --> Level0ArchitectBranch0["Architect [B0L0]"]
        Level0ArchitectBranch0 -- "Proposed interface + test analysis" --> InterfaceTesterBranch0["Interface Test Prototyper [B0L0]"]
        
        subgraph "Branch 0 Sub-Flow"
            InterfaceTesterBranch0 -- "Test results (success/failure)" --> Level0ArchitectBranch0
            InterfaceTesterBranch0 -- "Validated tests" --> TestBankBranch0[("Test Bank [B0L0]")]
        end
        
        InterfaceTesterBranch0 -- "Validated interfaces" --> Level1ArchitectBranch0["Architect [B0L1]"]
        Level1ArchitectBranch0 -- "Proposed interfaces + test analysis" --> InterfaceTesterBranch0Level1["Interface Test Prototyper [B0L1]"]
        InterfaceTesterBranch0Level1 -- "Test results (success/failure)" --> Level1ArchitectBranch0
        InterfaceTesterBranch0Level1 -. "Validated interfaces" .-> LevelmArchitectBranch0["Architect [B0Lm]"]
        LevelmArchitectBranch0 -- "Proposed interfaces + test analysis" --> InterfaceTesterBranch0Levelm["Interface Test Prototyper [B0Lm]"]
        InterfaceTesterBranch0Levelm -- "Test results (success/failure)" --> LevelmArchitectBranch0
    end
    
    RenovationTesterBranch0 -- "Old/modified validated interfaces" --> RenovationArchitectBranch1
    

    
    RenovationTesterBranch0 -- "Test results (success/failure)" --> EntityAnalyst
    
    RenovationTesterBranch1 -- "Old/modified validated interfaces" --> RenovationArchitectBranch2
    

    
    %% ─────────────────────────────────────────────────────
    %% BRANCH 1 - Parallel Flow
    %% ─────────────────────────────────────────────────────
    
    subgraph "Branch 1 Flow"
        RenovationArchitectBranch1["Renovation Architect [B1L0]"]
        
        RenovationArchitectBranch1 -- "[B1] Proposed interfaces + test analyses" --> RenovationTesterBranch1["Renovation Interface Test Prototyper [B1L0]"]
        
        RenovationTesterBranch1 -- "Test results (success/failure)" --> RenovationArchitectBranch1
        RenovationTesterBranch1 -- "Validated tests" --> TestBank1[("Renovation Test Bank [B1L0]")]
        RenovationTesterBranch1 -- "New Validated Interfaces" --> Level0ArchitectBranch1["Architect [B1L0]"]
        Level0ArchitectBranch1 -- "Proposed interface + test analysis" --> InterfaceTesterBranch1["Interface Test Prototyper [B1L0]"]
        
        subgraph "Branch 1 Sub-Flow"
            InterfaceTesterBranch1 -- "Test results (success/failure)" --> Level0ArchitectBranch1
            InterfaceTesterBranch1 -- "Validated tests" --> TestBankBranch1[("Test Bank [B1L0]")]
        end
        
        InterfaceTesterBranch1 -- "Validated interfaces" --> Level1ArchitectBranch1["Architect [B1L1]"]
        Level1ArchitectBranch1 -- "Proposed interfaces + test analysis" --> InterfaceTesterBranch1Level1["Interface Test Prototyper [B1L1]"]
        InterfaceTesterBranch1Level1 -- "Test results (success/failure)" --> Level1ArchitectBranch1
        InterfaceTesterBranch1Level1 -. "Validated interfaces" .-> LevelmArchitectBranch1["Architect [B1Lm]"]
        LevelmArchitectBranch1 -- "Proposed interfaces + test analysis" --> InterfaceTesterBranch1Levelm["Interface Test Prototyper [B1Lm]"]
        InterfaceTesterBranch1Levelm -- "Test results (success/failure)" --> LevelmArchitectBranch1
    end
    
    RenovationTesterBranch2 -- "Old/modified validated interfaces" --> RenovationArchitectBranch3
    

    
    %% ─────────────────────────────────────────────────────
    %% BRANCH 2 - Parallel Flow
    %% ─────────────────────────────────────────────────────
    
    subgraph "Branch 2 Flow"
        RenovationArchitectBranch2["Renovation Architect [B2L0]"]
        
        RenovationArchitectBranch2 -- "[B2] Proposed interfaces + test analyses" --> RenovationTesterBranch2["Renovation Interface Test Prototyper [B2L0]"]
        
        RenovationTesterBranch2 -- "Test results (success/failure)" --> RenovationArchitectBranch2
        RenovationTesterBranch2 -- "Validated tests" --> TestBank2[("Renovation Test Bank [B2L0]")]
        RenovationTesterBranch2 -- "New Validated Interfaces" --> Level0ArchitectBranch2["Architect [B2L0]"]
        Level0ArchitectBranch2 -- "Proposed interface + test analysis" --> InterfaceTesterBranch2["Interface Test Prototyper [B2L0]"]
        
        subgraph "Branch 2 Sub-Flow"
            InterfaceTesterBranch2 -- "Test results (success/failure)" --> Level0ArchitectBranch2
            InterfaceTesterBranch2 -- "Validated tests" --> TestBankBranch2[("Test Bank [B2L0]")]
        end
        
        InterfaceTesterBranch2 -- "Validated interfaces" --> Level1ArchitectBranch2["Architect [B2L1]"]
        Level1ArchitectBranch2 -- "Proposed interfaces + test analysis" --> InterfaceTesterBranch2Level1["Interface Test Prototyper [B2L1]"]
        InterfaceTesterBranch2Level1 -- "Test results (success/failure)" --> Level1ArchitectBranch2
        InterfaceTesterBranch2Level1 -. "Validated interfaces" .-> LevelmArchitectBranch2["Architect [B2Lm]"]
        LevelmArchitectBranch2 -- "Proposed interfaces + test analysis" --> InterfaceTesterBranch2Levelm["Interface Test Prototyper [B2Lm]"]
        InterfaceTesterBranch2Levelm -- "Test results (success/failure)" --> LevelmArchitectBranch2
    end
    
    RenovationTesterBranch3 -- "Old/modified validated interfaces" --> RenovationArchitectBranch4
    

    
    %% ─────────────────────────────────────────────────────
    %% BRANCH 3 - Parallel Flow
    %% ─────────────────────────────────────────────────────
    
    subgraph "Branch 3 Flow"
        RenovationArchitectBranch3["Renovation Architect [B3L0]"]
        
        RenovationArchitectBranch3 -- "[B3] Proposed interfaces + test analyses" --> RenovationTesterBranch3["Renovation Interface Test Prototyper [B3L0]"]
        
        RenovationTesterBranch3 -- "Test results (success/failure)" --> RenovationArchitectBranch3
        RenovationTesterBranch3 -- "Validated tests" --> TestBank3[("Renovation Test Bank [B3L0]")]
        RenovationTesterBranch3 -- "New Validated Interfaces" --> Level0ArchitectBranch3["Architect [B3L0]"]
        Level0ArchitectBranch3 -- "Proposed interface + test analysis" --> InterfaceTesterBranch3["Interface Test Prototyper [B3L0]"]
        
        subgraph "Branch 3 Sub-Flow"
            InterfaceTesterBranch3 -- "Test results (success/failure)" --> Level0ArchitectBranch3
            InterfaceTesterBranch3 -- "Validated tests" --> TestBankBranch3[("Test Bank [B3L0]")]
        end
        
        InterfaceTesterBranch3 -- "Validated interfaces" --> Level1ArchitectBranch3["Architect [B3L1]"]
        Level1ArchitectBranch3 -- "Proposed interfaces + test analysis" --> InterfaceTesterBranch3Level1["Interface Test Prototyper [B3L1]"]
        InterfaceTesterBranch3Level1 -- "Test results (success/failure)" --> Level1ArchitectBranch3
        InterfaceTesterBranch3Level1 -. "Validated interfaces" .-> LevelmArchitectBranch3["Architect [B3Lm]"]
        LevelmArchitectBranch3 -- "Proposed interfaces + test analysis" --> InterfaceTesterBranch3Levelm["Interface Test Prototyper [B3Lm]"]
        InterfaceTesterBranch3Levelm -- "Test results (success/failure)" --> LevelmArchitectBranch3
    end
    
    %% ─────────────────────────────────────────────────────
    %% BRANCH 4 - Parallel Flow
    %% ─────────────────────────────────────────────────────
    
    subgraph "Branch 4 Flow"
        RenovationArchitectBranch4["Renovation Architect [B4L0]"]
        
        RenovationArchitectBranch4 -- "[B4] Proposed interfaces + test analyses" --> RenovationTesterBranch4["Renovation Interface Test Prototyper [B4L0]"]
        
        RenovationTesterBranch4 -- "Test results (success/failure)" --> RenovationArchitectBranch4
        RenovationTesterBranch4 -- "Validated tests" --> TestBank4[("Renovation Test Bank [B4L0]")]
        RenovationTesterBranch4 -- "New Validated Interfaces" --> Level0ArchitectBranch4["Architect [B4L0]"]
        Level0ArchitectBranch4 -- "Proposed interface + test analysis" --> InterfaceTesterBranch4["Interface Test Prototyper [B4L0]"]
        
        subgraph "Branch 4 Sub-Flow"
            InterfaceTesterBranch4 -- "Test results (success/failure)" --> Level0ArchitectBranch4
            InterfaceTesterBranch4 -- "Validated tests" --> TestBankBranch4[("Test Bank [B4L0]")]
        end
        
        InterfaceTesterBranch4 -- "Validated interfaces" --> Level1ArchitectBranch4["Architect [B4L1]"]
        Level1ArchitectBranch4 -- "Proposed interfaces + test analysis" --> InterfaceTesterBranch4Level1["Interface Test Prototyper [B4L1]"]
        InterfaceTesterBranch4Level1 -- "Test results (success/failure)" --> Level1ArchitectBranch4
        InterfaceTesterBranch4Level1 -. "Validated interfaces" .-> LevelmArchitectBranch4["Architect [B4Lm]"]
        LevelmArchitectBranch4 -- "Proposed interfaces + test analysis" --> InterfaceTesterBranch4Levelm["Interface Test Prototyper [B4Lm]"]
        InterfaceTesterBranch4Levelm -- "Test results (success/failure)" --> LevelmArchitectBranch4
    end
    
    %% ─────────────────────────────────────────────────────
    %% BRANCH n - November Flow (Recursive Pattern)
    %% ─────────────────────────────────────────────────────
    
    subgraph "Branch n Flow"
        RenovationArchitectBranchn["Renovation Architect [BnL0]"]
        
        RenovationArchitectBranchn -- "[Bn] Proposed interfaces + test analyses" --> RenovationTesterBranchn["Renovation Interface Test Prototyper [BnL0]"]
        
        RenovationTesterBranchn -- "Test results (success/failure)" --> RenovationArchitectBranchn
        RenovationTesterBranchn -- "Validated tests" --> TestBankn[("Renovation Test Bank [BnL0]")]
        RenovationTesterBranchn -- "New Validated Interfaces" --> Level0ArchitectBranchn["Architect [BnL0]"]
        Level0ArchitectBranchn -- "Proposed interface + test analysis" --> InterfaceTesterBranchn["Interface Test Prototyper [BnL0]"]
        
        subgraph "Branch n Sub-Flow"
            InterfaceTesterBranchn -- "Test results (success/failure)" --> Level0ArchitectBranchn
            InterfaceTesterBranchn -- "Validated tests" --> TestBankBranchn[("Test Bank [BnL0]")]
        end
        
        InterfaceTesterBranchn -- "Validated interfaces" --> Level1ArchitectBranchn["Architect [BnL1]"]
        Level1ArchitectBranchn -- "Proposed interfaces + test analysis" --> InterfaceTesterBranchnLevel1["Interface Test Prototyper [BnL1]"]
        InterfaceTesterBranchnLevel1 -- "Test results (success/failure)" --> Level1ArchitectBranchn
        InterfaceTesterBranchnLevel1 -. "Validated interfaces" .-> LevelmArchitectBranchn["Architect [BnLm]"]
        LevelmArchitectBranchn -- "Proposed interfaces + test analysis" --> InterfaceTesterBranchnLevelm["Interface Test Prototyper [BnLm]"]
        InterfaceTesterBranchnLevelm -- "Test results (success/failure)" --> LevelmArchitectBranchn
    end
    
    %% Implementation Summary Flow for Branch n (Backwards Consolidation)
    %% Branch n: Level m -> Level 1 -> Level 0 -> Renovation Architect
    LevelmArchitectBranchn -. "Implementation summary [BnLm]" .-> Level1ArchitectBranchn
    Level1ArchitectBranchn -. "Implementation summary [BnL1]" .-> Level0ArchitectBranchn
    Level0ArchitectBranchn -. "Implementation summary [BnL0]" .-> RenovationArchitectBranchn
    
    %% Dotted connections from Branch 4 to Branch n
    RenovationTesterBranch4 -. "Old/modified validated interfaces" .-> RenovationArchitectBranchn
    RenovationTesterBranch4Levelm -. "Test results (success/failure)" .-> RenovationTesterBranch4
    
    %% Implementation Summary Flow (Backwards Consolidation)
    %% Branch 4: Level m -> Level 1 -> Level 0 -> Renovation Architect
    LevelmArchitectBranch4 -. "Implementation summary [B4Lm]" .-> Level1ArchitectBranch4
    Level1ArchitectBranch4 -. "Implementation summary [B4L1]" .-> Level0ArchitectBranch4
    Level0ArchitectBranch4 -. "Implementation summary [B4L0]" .-> RenovationArchitectBranch4
    
    %% Branch 3: Level m -> Level 1 -> Level 0 -> Renovation Architect
    LevelmArchitectBranch3 -. "Implementation summary [B3Lm]" .-> Level1ArchitectBranch3
    Level1ArchitectBranch3 -. "Implementation summary [B3L1]" .-> Level0ArchitectBranch3
    Level0ArchitectBranch3 -. "Implementation summary [B3L0]" .-> RenovationArchitectBranch3
    
    %% Branch 2: Level m -> Level 1 -> Level 0 -> Renovation Architect
    LevelmArchitectBranch2 -. "Implementation summary [B2Lm]" .-> Level1ArchitectBranch2
    Level1ArchitectBranch2 -. "Implementation summary [B2L1]" .-> Level0ArchitectBranch2
    Level0ArchitectBranch2 -. "Implementation summary [B2L0]" .-> RenovationArchitectBranch2
    
    %% Branch 1: Level m -> Level 1 -> Level 0 -> Renovation Architect
    LevelmArchitectBranch1 -. "Implementation summary [B1Lm]" .-> Level1ArchitectBranch1
    Level1ArchitectBranch1 -. "Implementation summary [B1L1]" .-> Level0ArchitectBranch1
    Level0ArchitectBranch1 -. "Implementation summary [B1L0]" .-> RenovationArchitectBranch1
    
    %% Branch 0: Level m -> Level 1 -> Level 0 -> Entity Analyst (Renovation Architect)
    LevelmArchitectBranch0 -. "Implementation summary [B0Lm]" .-> Level1ArchitectBranch0
    Level1ArchitectBranch0 -. "Implementation summary [B0L1]" .-> Level0ArchitectBranch0
    Level0ArchitectBranch0 -. "Implementation summary [B0L0]" .-> EntityAnalyst
    
    %% Branch Implementation Summary Flow (Cross-Branch Consolidation)
    %% From bottom branch to top branch: Branch n -> Branch 4 -> Branch 3 -> Branch 2 -> Branch 1 -> Branch 0
    RenovationArchitectBranchn -. "Branch implementation summary [Bn]" .-> RenovationArchitectBranch4
    RenovationArchitectBranch4 -. "Branch implementation summary [B4]" .-> RenovationArchitectBranch3
    RenovationArchitectBranch3 -. "Branch implementation summary [B3]" .-> RenovationArchitectBranch2
    RenovationArchitectBranch2 -. "Branch implementation summary [B2]" .-> RenovationArchitectBranch1
    RenovationArchitectBranch1 -. "Branch implementation summary [B1]" .-> EntityAnalyst
    

    


    %% Styling (purely visual – tweak as you like)
    classDef artifact fill:#f9f,stroke:#333,stroke-width:1px,color:#000;
    classDef recursive fill:#e6f3ff,stroke:#0066cc,stroke-width:2px,stroke-dasharray: 5 5,color:#000;
    classDef november fill:#fff2e6,stroke:#cc6600,stroke-width:2px,stroke-dasharray: 3 3,color:#000;
    classDef database fill:#e8f4f8,stroke:#0066cc,stroke-width:2px,color:#000;
    class Roadmap database;
    class TestBank0 artifact;
    class TestBank1 artifact;
    class TestBank2 artifact;
    class TestBank3 artifact;
    class TestBank4 artifact;
    class TestBank5 artifact;
    class TestBank artifact;
    class TestBankLevel1 artifact;
    class TestBankLevel2 artifact;
    class TestBankLevel3 artifact;
    class TestBankLevel4 artifact;
    class TestBankLevel5 artifact;
    class LevelmArchitectBranch0 recursive;
    class LevelmArchitectBranch1 recursive;
    class LevelmArchitectBranch2 recursive;
    class LevelmArchitectBranch3 recursive;
    class LevelmArchitectBranch4 recursive;
    class InterfaceTesterBranch0Level1 recursive;
    class InterfaceTesterBranch0Levelm recursive;
    class InterfaceTesterBranch1Levelm recursive;
    class InterfaceTesterBranch2Levelm recursive;
    class InterfaceTesterBranch3Levelm recursive;
    class InterfaceTesterBranch4Levelm recursive;
    class RenovationArchitectBranchn november;
    class RenovationTesterBranchn november;
    class Level0ArchitectBranchn november;
    class InterfaceTesterBranchn november;
    class Level1ArchitectBranchn november;
    class InterfaceTesterBranchnLevel1 november;
    class LevelmArchitectBranchn november;
    class InterfaceTesterBranchnLevelm november;
    class TestBankn november;
    class TestBankBranchn november;
    class Level1ArchitectBranchn november;
    class InterfaceTesterBranchnLevel1 november;