import class_blockchain
import database_connection
import batch


def print_menu():
    print("1. Create blockchain")
    print("2. Remove blockchain collection")
    print("3. Enter new slaughter record")
    print("4. Exit")


def main():
    # Connect to MongoDB and get database
    database = database_connection.connect_db()
    print(database_connection.batchNumberToHash(database, '42342'))
    while True:
        print_menu()
        choice = input("Enter your choice (1-4): ")
        if choice == '1':
            print("You selected Option 1.")
            # Blockchain creation
            blockchain = class_blockchain.Blockchain(database)
            # Get documents from batches collection and add to blockchain
            batches_collection = database_connection.getBatches(database)
            # Convert each batch record to blocks and store them in blockchain collection
            for batch_info in batches_collection:
                print(database_connection.batchNumberToHash(database, batch_info['batchNumber']))
                if database_connection.batchNumberToHash(database, batch_info['batchNumber']) is None:
                    batch.batch_handle(blockchain, batch_info)
            blockchain.print_blockchain()
        elif choice == '2':
            print("You selected Option 2.")
            database['blockchain'].drop()
        elif choice == '3':
            print("You selected Option 3.")
            batch.addNewSlaughter(database, '310520')
        elif choice == '4':
            print("Exiting the menu. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
