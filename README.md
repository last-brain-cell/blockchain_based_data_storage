## Decentralized File Storage using Blockchain

### Application Setup

1. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch the server/peer in one terminal:
   ```bash
   python peer.py
   ```

3. Start the client in another terminal:
   ```bash
   python run_app.py
   ```
   
4. Or just run the docker-compose if you have docker 

### Project Overview

This is a decentralized file storage web application utilizing blockchain technology. Users can securely upload and download files, ensuring data integrity and preventing unauthorized modifications.

### Blockchain Significance

Blockchain provides a secure means of storing digital information, incorporating consensus algorithms and block validation. This application utilizes SHA256 for security and implements a proof of work consensus algorithm.

### Proof of Work Algorithms

Two proof of work algorithms are implemented, each employing different nonce calculation methods. The first algorithm generates a random nonce, while the second increments the nonce by one.

### On-chain vs. Off-chain Blockchain

This implementation adopts an on-chain blockchain approach, storing file data directly within blocks. While on-chain blockchain offers heightened security and straightforward data recovery, it may demand more resources. Off-chain blockchain solutions store data externally but might compromise some security features.
