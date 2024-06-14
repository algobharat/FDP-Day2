import logging
import random
import algokit_utils
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from algosdk import transaction

logger = logging.getLogger(__name__)


# define deployment behaviour based on supplied app spec
def deploy(
    algod_client: AlgodClient,
    indexer_client: IndexerClient,
    app_spec: algokit_utils.ApplicationSpecification,
    deployer: algokit_utils.Account,
) -> None:
    from smart_contracts.artifacts.hello_world.client import (
        HelloWorldClient,
    )

    algod_address = "https://testnet-api.algonode.cloud"

    algod_token = "a" * 64


    algod_client = AlgodClient(algod_token,algod_address)

    deployer_mnemonic = "banner enlist wide have awake rail resource antique arch tonight pilot abuse file metal canvas beyond antique apart giant once slight ice beef able uncle"  # Replace with your TestNet account mnemonic

    deployer = algokit_utils.get_account_from_mnemonic(deployer_mnemonic)

    app_client = HelloWorldClient(
        algod_client,
        creator=deployer,
        indexer_client=indexer_client,
    )

    app_client.deploy(
        on_schema_break=algokit_utils.OnSchemaBreak.AppendApp,
        on_update=algokit_utils.OnUpdate.AppendApp,
    )
    name = "world"
    response = app_client.hello(name=name)
    logger.info(
        f"Called hello on {app_spec.contract.name} ({app_client.app_id}) "
        f"with name={name}, received: {response.return_value}"
    )

    firnum = 100
    secnum = 200
    response = app_client.addition(firnum=firnum,secnum=secnum)
    logger.info(
        f"Called Addition on {app_spec.contract.name} ({app_client.app_id}) "
        f"with Values={firnum,secnum}, received: {response.return_value}"
    )


    #asset creation

    # Asset Creation (Token)
    # Asset Parameter
    
    sp = algod_client.suggested_params()
    unsigned_txn = transaction.AssetCreateTxn(
        sender = deployer.address,
        sp = sp,
        total = 50,
        decimals = 0,
        default_frozen = False,
        asset_name = "DrasToken",
        unit_name = "DSPT",
        manager = deployer.address,
        clawback = deployer.address,
    )

    #sign transaction
    signed_txn = unsigned_txn.sign(deployer.private_key)
    print("signed TXN : ",signed_txn)

    #submit transaction
    txid = algod_client.send_transaction(signed_txn)
    print("successfully sent transaction with txID: {}".format(txid))
 
    while True:
        #rowid = rowid + 1
        temperature = random.randint(0, 250)
        response = app_client.temperature(temperature=temperature)
        print(response.tx_id)
    time.sleep(800)
