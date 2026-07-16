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
        mint_address = Pubkey.from_string(ca)

        response = client.get_account_info(mint_address)

        if response.value is None:
            result["risk"] = "INVALID TOKEN"
            return result


        data = response.value.data


        # SPL Token Mint Account layout
        # Byte 0-3 = mint authority option
        # Byte 4-35 = mint authority address
        # Byte 36-43 = supply
        # Byte 44 = decimals
        # Byte 45-48 = initialized
        # Byte 46-49 = freeze authority option

        mint_option = int.from_bytes(
            data[0:4],
            byteorder="little"
        )


        freeze_option = int.from_bytes(
            data[46:50],
            byteorder="little"
        )


        # Mint Authority
        if mint_option == 0:
            result["mint_authority"] = "OFF ✅"
        else:
            result["mint_authority"] = "ON ⚠️"


        # Freeze Authority
        if freeze_option == 0:
            result["freeze_authority"] = "OFF ✅"
        else:
            result["freeze_authority"] = "ON ⚠️"



        # Risk calculation sederhana

        risk_score = 0


        if mint_option != 0:
            risk_score += 1


        if freeze_option != 0:
            risk_score += 1



        if risk_score == 0:
            result["risk"] = "LOW 🟢"

        elif risk_score == 1:
            result["risk"] = "MEDIUM 🟡"

        else:
            result["risk"] = "HIGH 🔴"



        return result


    except Exception as e:
        print("Security Error:", e)
        return result