import random

import ksuid


ADMIN_USER_LOGIN = "root"
ADMIN_USER_PASSWORD = "root"
ADMIN_USER_EMAIL = ""

DEMO_USER_NAME = "Demo User"
DEMO_USER_LOGIN = "demo@gmail.com"
DEMO_USER_PASSWORD = "demo"
DEMO_USER_EMAIL = ""
DEMO_USER_UID = "0608e5abd7d361fbd16e68d89822f81a3252623f"


DEMO_NODE_NAME = "Demo collecting node"
DEMO_NODE_DESCRIPTION = "Node for demo mode"

DEMO_DEVICE_NAME = "Demo device"
DEMO_DEVICE_DESCRIPTION = "Device for demo mode"

DEMO_DEVICE_WRITE_TOKEN = "rLVNYnYKUgVF4QL7QPQwb4DbLV"
DEMO_DEVICE_READ_TOKEN = "rLY07TL8rh1sYH1fH8zXeqDP4i"


DEMO_CONFIGURATION = [
    {
        "dcn_name": DEMO_NODE_NAME,
        "dcn_description": DEMO_NODE_DESCRIPTION,
        "devices": [
            {
                "dcd_name": DEMO_DEVICE_NAME,
                "dcd_description": DEMO_DEVICE_DESCRIPTION,
                "write_token": DEMO_DEVICE_WRITE_TOKEN,
                "read_token": DEMO_DEVICE_READ_TOKEN
            }
        ]
    },

    {
        "dcn_name": "Second DCN",
        "dcn_description": "Second DCN for demo configuration",
        "devices": [
            {
                "dcd_name": "Second device",
                "dcd_description": "Second device for demo configuration",
                "write_token": "rYkcCbBnpBtuaR353eLy2udjFS",
                "read_token": "rYkkI4fUMF59DPL6YNjiKA0fZN"
            }
        ]
    },

    {
        "dcn_name": "Third DCN (W/O)",
        "dcn_description": "Third DCN for demo configuration (write only)",
        "devices": [
            {
                "dcd_name": "Third device (W/O)",
                "dcd_description": "Third device for demo configuration (W/O)",
                "write_token": "rYkw7ohCQOD33VqSA1CyAWX0ey",
                "read_token": None
            },

            {
                "dcd_name": "Fourth device (W/O)",
                "dcd_description": "Fourth device for demo configuration (W/O)",
                "write_token": "rYl62gSLXLsalya2mNzO1atFZ9",
                "read_token": None
            }
        ]
    }
]


POSSIBLE_TEST_PARAMS_NAME = [
    "foo",
    "boo",
    "zoo",
    "boom",
    "badum",
    "tsss",
    "test",
    "temp",
    "alfa",
    "bravo",
    "charlie",
    "units"
]

POSSIBLE_PARAMS_VALUE = [
    "value",
    "rpx",
    (lambda: str(ksuid.ksuid())),
    (lambda: ksuid.ksuid().toBase62()),
    (lambda: str(random.randint(1, 1000000000))),
    (lambda: random.choice(["true", "false"])),
    (lambda: random.choice(["C", "F"])),
    (lambda: str(round(random.uniform(-20, 40), 2)))
]
