# Traceability Blockchain

A Python-based blockchain implementation designed for livestock and meat industry traceability. This system ensures the integrity, security, and transparency of batch records, including vaccinations, breeding stages, and slaughter data.

## 🌟 Features

- **Custom Blockchain Core**: Implements a functional blockchain with blocks containing index, timestamp, encrypted data, and cryptographic hashes (SHA-256).
- **Data Encryption**: Utilizes the `cryptography` library (Fernet) to encrypt sensitive batch information before storing it on the chain.
- **Relational Linking**: Uses "Non-Consecutive Hashes" to link specific events (like a vaccination) back to its parent batch record, enabling easy audit trails.
- **Business Logic Validation**: Includes rules to prevent illegal state transitions (e.g., a slaughter record can only be added if breeding exit requirements are met).
- **MongoDB Integration**: Seamlessly connects to MongoDB to fetch raw batch data and store the finalized blockchain.

## 🏗 Architecture

- **`main.py`**: The entry point providing a CLI menu for managing the blockchain.
- **`class_blockchain.py`**: Contains the `Block` and `Blockchain` class definitions.
- **`batch.py`**: Handles the logic for converting database records into blockchain blocks and applying validation rules.
- **`database_connection.py`**: Manages connection to MongoDB and CRUD operations for blocks and batches.
- **`encryption.py`**: Handles key generation, encryption, and decryption of data.

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- **MongoDB**: Must be installed and running.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NickCh11/traceability-blockchain.git
   cd traceability-blockchain
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 🗄️ Database Setup

The application expects a MongoDB instance running at `localhost:27017`.

1. Create a database named `prodKoMeat`.
2. Create a collection named `batches`.
3. The `batches` collection should contain documents with the following structure (at minimum):
   ```json
   {
     "batchNumber": "310520",
     "vaccination": [],
     "stageOfBreeding": [{"exit": true}],
     "stageOfSlaughter": []
   }
   ```
   *Note: The application will automatically create the `blockchain` collection upon the first run.*

### Running the App

```bash
python main.py
```

## 🛠 Usage

Upon running `main.py`, you will be presented with the following options:

1. **Create blockchain**: Fetches records from the `batches` collection and converts them into an immutable blockchain.
2. **Remove blockchain collection**: Drops the `blockchain` collection from MongoDB to reset the chain.
3. **Enter new slaughter record**: Adds a new slaughter event to an existing batch after validating the rules.
4. **Exit**: Closes the application.

## 🔒 Security

Data integrity is maintained using SHA-256 hashing. Each block points to the hash of the previous block, making the chain immutable. Additionally, the data field of each block is encrypted using a local `encryption_key.key`. **Never share or lose this key, as it is required to decrypt the blockchain data.**

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
