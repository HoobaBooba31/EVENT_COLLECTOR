from api_keys import creating_api_key
import asyncio

def main():
    return asyncio.run(creating_api_key())

if __name__ == "__main__":
    print(main())
    

#     print(asyncio.run(main(bytes("LOL", encoding="utf-8"))))

