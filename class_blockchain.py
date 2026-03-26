import hashlib
import json
import datetime

import database_connection
import encryption


class Block:
    def __init__(self, index, data, data_type, previous_hash, timestamp=None, previous_non_consecutive_hash=None):
        self.index = index
        self.timestamp = timestamp or datetime.datetime.utcnow().timestamp()
        self.data = data
        self.data_type = data_type
        self.previous_hash = previous_hash
        self.previous_non_consecutive_hash = previous_non_consecutive_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "data_type": self.data_type,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "previous_non_consecutive_hash": self.previous_non_consecutive_hash
        }


class Blockchain:
    def __init__(self, database):
        self.chain = []
        self.database = database
        self.encryption_key = encryption.generate_encyption_key()

        genesis_block = Block(0, "Genesis Block", 'genesis', 0)
        genesis_block.data = encryption.encrypt_data(self.encryption_key, genesis_block.data)
        self.chain.append(genesis_block)
        if 'blockchain' not in database.list_collection_names():
            database_connection.storeBlock(self.database, genesis_block.to_dict())

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data, data_type, previous_non_consecutive_hash=None):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), data, data_type, previous_block.hash,
                          previous_non_consecutive_hash=previous_non_consecutive_hash)
        new_block.data = encryption.encrypt_data(self.encryption_key, data)
        self.chain.append(new_block)
        database_connection.storeBlock(self.database, new_block.to_dict())
        return new_block

    def print_blockchain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {datetime.datetime.fromtimestamp(block.timestamp)}")
            print(f"Data: {block.data}")
            print(f"Data Type: {block.data_type}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            if block.previous_non_consecutive_hash:
                print(f"Previous Non-Consecutive Hash: {block.previous_non_consecutive_hash}")
            print("-" * 50)
