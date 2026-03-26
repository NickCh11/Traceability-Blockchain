import database_connection
import class_blockchain
import encryption


def batch_handle(blockchain, batch):
    main_info_block = batch_main_info(blockchain, batch)  # Handles the main info of batch
    batch_vaccination_info(blockchain, batch, main_info_block)  # Handles the vaccination info of batch
    batch_stageOfBreeding_info(blockchain, batch, main_info_block)  # Handles the stage of breeding info of batch
    batch_slaughter_info(blockchain, batch, main_info_block)  # Handles the slaughters of batch
    return blockchain


# Convert main info into blocks
def batch_main_info(blockchain, batch):
    database_connection.convert_to_strings(batch)
    main_info = {k: v for k, v in batch.items() if not isinstance(v, list)}  # Keep basic info about batch
    return blockchain.add_block(main_info, 'main_info')


# Convert vaccinations into blocks
def batch_vaccination_info(blockchain, batch, main_info_block):
    database_connection.convert_to_strings(batch['vaccination'])
    for vaccination in batch['vaccination']:
        blockchain.add_block(vaccination, 'vaccination', previous_non_consecutive_hash=main_info_block.hash)


# Convert breedings into blocks
def batch_stageOfBreeding_info(blockchain, batch, main_info_block):
    database_connection.convert_to_strings(batch['stageOfBreeding'])
    for stage in batch['stageOfBreeding']:
        blockchain.add_block(stage, 'breeding', previous_non_consecutive_hash=main_info_block.hash)


# Convert slaughters into blocks
def batch_slaughter_info(blockchain, batch, main_info_block):
    if len(batch['stageOfSlaughter']) != 0:
        if slaughter_Rules(batch):
            database_connection.convert_to_strings(batch['stageOfSlaughter'])
            for slaughters in batch['stageOfSlaughter']:
                blockchain.add_block(slaughters, 'slaughters', previous_non_consecutive_hash=main_info_block.hash)
        else:
            print('Slaughters not allowed in this batch')


# Slaughter rules for local add of slaughter checking local blockchain
def slaughter_Rules(batch):  # Rule node for slaughter
    if len(batch['stageOfBreeding']) > 0 and batch['stageOfBreeding'][0]['exit']:
        return True


# Add a new slaughter based a batch
def addNewSlaughter(database, batchNumber):
    slaughter_data = {"slaughtered": True,
                      "delete": False,
                      "deletedAt": None,
                      "totalAnimals": 50,
                      "slaughterWeight": 80,
                      "slaughterAnimalAge": None,
                      "slaughterDate": 1622459889,
                      "slaughterPlace": None,
                      "slaughterHealthStatus": None,
                      "slaughterPlaceCode": "S120",
                      "slughterCountryOfOrigin": None,
                      "slaughterAnimalCategory": "210-ΧΟΙΡΟΣ",
                      "slaughterTurn": None,
                      "user": {
                          "$oid": "5fd08bde58806ca2b5805d3b"
                      },
                      "updatedAt": {
                          "$date": "2021-05-31T11:18:28.518Z"
                      },
                      "createdAt": {
                          "$date": "2021-05-31T11:18:28.518Z"
                      }
                      }
    main_info_block = database_connection.batchNumberToHash(database, batchNumber)
    newSlaughter_Rules(database, main_info_block)
    previous_block = database_connection.getLatestBlock(database)
    if main_info_block is not None:
        if newSlaughter_Rules(database, main_info_block):
            new_block = class_blockchain.Block(previous_block['index'] + 1, slaughter_data,
                                               'slaughters',
                                               previous_hash=previous_block['hash'],
                                               previous_non_consecutive_hash=main_info_block['hash'])
            new_block.data = encryption.encrypt_data(encryption.generate_encyption_key(), slaughter_data)
            database_connection.storeBlock(database, new_block.to_dict())
            print('New slaughter added...')
        else:
            print('New slaughter cannot added...')


# Slaughter rules for remote add of slaughter checking blockchain collection
def newSlaughter_Rules(database, main_info_block):
    stageOfBreeding = list(database['blockchain'].find(
        {"data_type": "breeding", "previous_non_consecutive_hash": main_info_block['hash']}))
    if len(stageOfBreeding) != 0:
        return True
