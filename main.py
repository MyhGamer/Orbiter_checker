import asyncio
import aiohttp

async def get_total_points(session, address):
    url = f"https://api.orbiter.finance/points_system/v2/user/points?address={address}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            total_points = data.get('data', {}).get('total', 0)
            return total_points
        else:
            return None

async def process_addresses(wallet_addresses):
    total_points_sum = 0
    async with aiohttp.ClientSession() as session:
        tasks = [get_total_points(session, address) for address in wallet_addresses]
        total_points_list = await asyncio.gather(*tasks)

    for address, total_points in zip(wallet_addresses, total_points_list):
        if total_points is not None:
            print(f"{address} - total: {total_points}")
            total_points_sum += total_points
        else:
            print(f"Failed to retrieve data for address: {address}")

    print(f"\nSum of \"total\": {total_points_sum}")

def main():
    # Replace 'wallets.txt' with the path to your text file containing wallet addresses
    with open('wallets.txt', 'r') as file:
        wallet_addresses = [line.strip() for line in file.readlines()]

    asyncio.run(process_addresses(wallet_addresses))

if __name__ == "__main__":
    main()
