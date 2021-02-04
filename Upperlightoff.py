# -*- coding: utf-8 -*-
#!/usr/bin/python3
# install pip if not installed
# pip3 install meross-iot
# This is tested on Windows 10, Linux see bottom of script

import asyncio
from time import sleep

from meross_iot.http_api import MerossHttpClient
from meross_iot.manager import MerossManager

# Parameters

device_type = 'mss710'                   # Meross device used
device_name = '3D printer upper light'   # Meross device name 

EMAIL = "email"              # Meross account log in
PASSWORD = "Password"

async def main():
    http_api_client = await MerossHttpClient.async_from_user_password(email=EMAIL, password=PASSWORD)
    manager = MerossManager(http_client=http_api_client)
    await manager.async_init()
    await manager.async_device_discovery()
    plugs = manager.find_devices(device_type=device_type)
    sleep(2)
    if len(plugs) < 1:
        print("No {device_type} plugs found...")
    else:
        plug_exsists = False
        x = 0
        for plug in plugs:
            if plug.name == device_name:
                plug_exsists = True
                plug_number = x
            x += 1
        if plug_exsists:
            dev = plugs[plug_number]
            await dev.async_turn_off(channel=0)
        else:
            print("Plug does not exsist")
    manager.close()
    await http_api_client.async_logout()

if __name__ == '__main__':
    # On Windows + Python 3.8, you should uncomment the following
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())           # Comment out on Linux
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
