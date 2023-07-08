# ABAC-SE-Scheme

- Graduation Thesis:  **Attribute-based access control and Searchable Encryption in NoSQL database**
- Supervisor: Ph.D Ngoc-Tu Nguyen [Scholar References](https://scholar.google.com/citations?hl=vi&user=baIb5JgAAAAJ&view_op=list_works&sortby=pubdate)
- Participation: Hồ Đắc Thanh Minh - Nguyễn Minh Hiển

## Abstraction

The use of untrusted third-party storage parties loses the ability to strictly control users as well as can not guarantee the integrity and security of data. Besides, the cloud infrastructure also has some errors such as configuration compatibility, attacks that can leak user's data. Therefore, encrypting before sending data to cloud platforms is now an effective solution to solve this problem.

With traditional encryption types such as symmetric encryption, asymmetric encryption, although meeting encryption capabilities, lacks the ability to control access to data. Attribute-Based Encryption (ABE) is an output encryption technique that solves this problem. ABE is developed in the direction of role-based access control (RBAC). The user must have attributes that are compatible with the access policy in order to read the encrypted document. However, ABE faces a number of challenges such as the computational cost of key generation, encryption, and decryption, and the ability to manage access policies. There have been many studies on these aspects and many authors have found solutions to improve and increase the efficiency of ABE such as ABE scheme with key revocation, ABE scheme using multiple certificates. Multi Authorization, the ABE schema supports efficient computation.

Besides the ability to control access, the search on the ciphertext is also a big challenge in the problem of data encryption. For plaintext the user only needs to send queries to the server to get the document, then the server will return the search results to the user. But after encryption, the data has become encrypted form that makes searching difficult and expensive. Searchable Encryption (SE) was born to solve this problem. SE allows encrypted data to be stored on a cloud server from an untrusted third-party service provider, while ensuring that users can search directly on the ciphertext with high precision. Many articles have been published to research on this issue and produce schemas to improve the efficiency of Searchable Encyrption such as schemas to support approximate search, schemas to support multiple keyword searches.

In this Graduation Thesis, the team researches a number of improved schemas to enhance the security and efficiency of attribute-based encryption schemes and cipher data search schemes. Thereby, the team will experiment with the model using NoSQL database management system in the real estate business environment and evaluate the effectiveness of the experiment on that management system.


## Context

**Thread Modal**

![](/assets/theardModal.png)

1. Untrusted Third-party (Cloud)
2. Adversary:
    - Interfere with the communication process between stakeholders.
    - Impersonate related parties.
    - Attack on the storage side (cloud).

**Propose Modal**

![](/assets/proposeModal.png)

## Implementation Details


### Attribute-base Access Control Scheme
**Algorithm**

![](/assets/abacScheme.png)

### Searchable Encryption Scheme
**Algorithm** 

![](/assets/seScheme.png)

**Diagram**

![](/assets/seSchemeDiagram.png)

### Implementation Structure

![](/assets/architecture.png)

## Keywords
`symmetric encryption`, `attribute-based encryption`, `searchable encryption`, `ciphertext policy attribute-based encryption`, `attribute-based access control`, `multi authority access control`, `user's attributes revocation`, `fuzzy search`, `multi-keyword search`, `untrusted third-party storage`, `NoSQL database`, `cloud storage`, `Microsoft Azure`, `Azure Container Group Instance`, `Azure Cosmos DB`
