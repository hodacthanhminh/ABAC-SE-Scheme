# Source structure
This repo will follow the structure below

```
.
├── cosmosInteraction                      // interaction methods with cosmosDb
│   ├── .env                        
│   │
│   └── ...
│
├── keyword                                // contain keyword extract from document 
│   ├── keyworddocument1.json                 
│   │
│   ├── ...
│   └── ...
│
├── oldCode                                // draft coding of Searchable Encryption
│
├── se                                     // Main module Searchable Encryption
│
├── storage                                // contain main artifact of source
│   │    
│   ├── 128          
│   │    
│   ├── 256
│   │   ├── index                         // include index encrypted by SE in 256bit
│   │   │
│   │   └── key                           // include key generated by SE in 256bit
│   │
│   ├── document                           // provided plain document for extracting keyword and applying ABAC
│   │
│   ├── encrypted                          // store encryptedDocument after applying ABAC
│   │
│   ├── keyword                            // store extracting keyword from plain document 
│   │
│   └── searchResult
│       ├── decrypted                     // store plain document after using ABAC to decrypt                     
│       │
│       └── encrypted                     // store search result document after search on cosmosDb
│           
└── README.md
```