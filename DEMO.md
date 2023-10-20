
```bash
arc-cli --help
```

## Login
```bash
arc-cli auth login --client-id=$CLIENT_ID --client-secret=$CLIENT_SECRET
```

```bash
arc-cli auth status
```

## Create Keys
```bash
arc-cli utils gen-stark-keys
```

```bash
arc-cli utils gen-eth-keys
```

## Register User
```bash
arc-cli users register threesigmxyz \
  --eth-key=0x5adc1f3d896ddbcbdae65dbd18ef2ab10d72bdda8012414806aa02204811d199 \
  --stark-key=0x49d42b646b4b048ee4c24b386b410c8e2c6cd03669b7c1f237b96a33ddc96db
```

```bash
eth_pub:
stark_pub:
```

arc-cli users register afonso@threesigma.xyz \
  --eth-key=0x4e7e001b4afd56d219c95d156a432c96f5776797e12f43eec2d598a225dad6b5 \
  --stark-key=
```

## Deposit Eth
```bash
arc-cli deposits deposit \
  --user-id=d75a22ee-75bd-4e43-ba5d-bf9ca9b2a024 \
  --asset-id=01e5a68e-da3e-44b5-b3c5-1ec29bd602e4 \
  --amount=10000 \
  --eth-private-key=0xb11a7f726e97b410280f2710e0e2fefafa8e53c2c975c2268af8770818371815
```

arc-cli 

```bash
arc-cli mints mint \
  --user-id=d75a22ee-75bd-4e43-ba5d-bf9ca9b2a024 \
  --asset-id=508f5084-a58c-4e55-9bb2-63bb9eb3fea0 \
  --amount=1 \
  --token-id=999901
```
```bash
arc-cli utils pedersen-hash \
  1740729136829561885683894917751815192814966525555656371386868611731128807883 \
  919869093895560023824014392670608914007817594969197822578496829435657368346 \
  --json
```

```bash
arc-cli utils pedersen-hash \
  2422460557091938808713946367355500260404495937317443380382672985795284033965 \
  168976971209324910088270776698114429106829914647771869169305379452790116384 \
  --json
```

## Deposit Eth Faucet
```bash
arc-cli deposits deposit \
  --user-id=07b3b817-65bb-4b9e-87b5-5becb8e55f15 \
  --asset-id=01e5a68e-da3e-44b5-b3c5-1ec29bd602e4 \
  --amount=10000000000 \
  --eth-private-key=0x5d1edcc5d09a1f4e67302ff42edf7f9c5b4338246d0a51e5749dbdf2540ab303
```

# Deposit 1ETH into demo account 1 (tic9a117s)
# Source of funds: 07b3b817-65bb-4b9e-87b5-5becb8e55f15
```bash
arc-cli deposits deposit \
  --user-id=398d37d0-4587-480c-93f4-570afac238d6 \
  --asset-id=01e5a68e-da3e-44b5-b3c5-1ec29bd602e4 \
  --amount=20000000000 \
  --eth-private-key=0x5d1edcc5d09a1f4e67302ff42edf7f9c5b4338246d0a51e5749dbdf2540ab303
```

arc-cli mints mint \
  --user-id=07b3b817-65bb-4b9e-87b5-5becb8e55f15 \
  --asset-id=508f5084-a58c-4e55-9bb2-63bb9eb3fea0 \
  --amount=1 \
  --token-id=949901

arc-cli transfers transfer \
  --sender-id=07b3b817-65bb-4b9e-87b5-5becb8e55f15 \
  --recipient-id=398d37d0-4587-480c-93f4-570afac238d6 \
  --asset-id=01e5a68e-da3e-44b5-b3c5-1ec29bd602e4 \
  --amount=1000000000 \
  --stark-private-key=0x71f479dfdfec57fbaca0dcbdb3d9e27b73d247ed27d8766aad2e0f795c2511a
