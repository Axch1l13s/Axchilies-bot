from solana.rpc.api import Client
from solders.pubkey import Pubkey

RPC = "https://api.mainnet-beta.solana.com"

client = Client(RPC)


def check_security(ca):

    result = {
        "mint_authority": "Unknown",
        "freeze_authority": "Unknown",
        "risk": "MEDIUM"
    }

    try:
        mint = Pubkey.from_string(ca)

        info = client.get_account_info(mint)

        if info.value is None:
            result["risk"] = "INVALID TOKEN"
            return result

        result["mint_authority"] = "Need Parse"
        result["freeze_authority"] = "Need Parse"

        return result

    except Exception as e:
        print("Security Error:", e)
        return result