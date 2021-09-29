import time
from Block import Block


class Blockchain:
    def __init__(self):
        self.difficulty = 3
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = self.find_valid_hash(genesis_block)
        self.chain.append(genesis_block)

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def add_new_transaction_list(self, transaction_list):
        self.unconfirmed_transactions.extend(transaction_list)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.chain[-1]

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        computed_hash = self.find_valid_hash(new_block)
        self.add_block(new_block, computed_hash)
        self.unconfirmed_transactions = []

    def find_valid_hash(self, block):
        block.nonce = 1
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, computed_hash):
        block.hash = computed_hash
        self.chain.append(block)

    def validate_chain(self):
        print("-----------------------")
        invalid = False
        for block in self.chain:
            validation_block = block.create_clone()

            actual_hash = validation_block.compute_hash()
            print("nonce:")
            print(block.nonce)
            if actual_hash == block.hash:
                print("hash:")
                print(block.hash)
                print("block validated")
            else:
                invalid = True
                print("invalid block")
            print("-----------------------")

        if invalid:
            print("invalid chain")
        else:
            print("chain validated")

        print("-----------------------")


if __name__ == '__main__':
    initial_time = time.time()

    bc = Blockchain()
    bc.add_new_transaction("transaction 1")
    bc.mine()
    bc.add_new_transaction("transaction 2")
    bc.mine()
    bc.add_new_transaction("transaction 3")
    bc.mine()
    bc.add_new_transaction_list(["transaction 4", "transaction 5"])
    bc.mine()

    bc.validate_chain()
    end_time = time.time() - initial_time
    print(end_time)