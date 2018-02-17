### Part 1: GENI Lab
For this part of the lab I used the [RSpec file](https://gist.githubusercontent.com/ffund/5b5165df52c342b7bd163d3c7ca76855/raw/70f6fb663a86dbe35a1d9bdc262428444e0f3d19/bitcoin.xml) provide in the [geni bitcoin tutorial](https://witestlab.poly.edu/blog/get-rich-on-fake-bitcoins/) to create a geni network with the network map as follows:

![geni bitcoin netmap](https://lh5.googleusercontent.com/9mJse-ROK1JpRsd2tP3UQgwc70FZTvxlgWqk_YbWxB8Z-1OhD5Ip4y0EcZeTiHBU04sT5KeHv0JzKSO8J3R4=w1920-h937)

After creating the network I was able to ssh into each node simultaneously: remotely controlling each node in my blockchain network. This allowed me to discover the nuances of how bitcoin is able to achieve consensus for transactions in their distributed network, and how a blockchain network handles conflicts in the blockchain.

This experiment was run using the `-regtest` flag for the `bitcoin-cli` command this allowed blocks to be generated on command for testing purposes, preventing unnecessary waste of electricity and time mining.      
#### How Bitcoin transaction become spendable.
After generating several blocks and seeing how the new blocks propagated through the network, I tested how a transaction is confirmed on the network. The transaction I sent was from node-0 to node-4. To do this I first had to obtain the wallet address for node-4; this was accomplished with the following command on node-4:
```
bellmj@node-4:~$ bitcoin-cli -regtest getbalance
1000.00000000
bellmj@node-4:~$ bitcoin-cli -regtest getnewaddress
n4avXCyvkSWPNc2z62S1uRX3QKa3mXN3Cv
```
After obtaining the wallet address for node-4, node-0 can now initiate a transaction to node-4, using the following command:
```
bellmj@node-0:~$ bitcoin-cli -regtest getbalance
50.00000000
bellmj@node-0:~$ bitcoin-cli -regtest sendtoaddress n4avXCyvkSWPNc2z62S1uRX3QKa3mXN3Cv 10.00
35c15a93d7c8c58da2f42bd868c88b777018d9a05c8936d4764f3be847944c9b
bellmj@node-0:~$ bitcoin-cli -regtest getbalance
39.99996160
```
One can see that balance of node-0 went down instantly, and that node-0 was provided a transaction number upon initialization of the transaction. However, this transaction has not been confirmed by the network yet. It is also important to node that the deduction from node-0's balance is slightly more than the amount that was sent; this is due to small transaction fee used to incentivize the miners in the network. The current status of this transaction is made apparent by checking the balance of node-4:
```
bellmj@node-4:~$ bitcoin-cli -regtest getbalance
1000.00000000
```
This is the same balance node-4 had before node-0 made its' transaction so we know this transaction is still unconfirmed.

In order for this transaction to be confirmed we need confirmations by the network. A confirmation is simply another blocked added to the chain, dependent on this transaction. This is possible since the blockchain used the entire previous blockchain hashed as partial input for the next block. This means that the transaction will be included in all subsequent blocks. After six new blocks have been added to the network including this new transaction, this transaction has been deemed sufficiently had to faked and therefore not able to be double spent. Six new blocks were added to the block chain using node-1 with:
```
bellmj@node-1:~$ bitcoin-cli -regtest generate 6
[
  "3632a70a7c71bd7332c8ddf8e8a710c47394d12ba6f3640cf549c1d49c39a261",
  "73489db20fca68a3f08e4e2f38e89a2d02ae5010b91220df734e9bf4fcecd305",
  "1bdfea8499742706bd67cf7c6e854d46b6c021c08303ae5335a960257bc97e92",
  "1d2b3c5e2e4e79533085f47c8749d3a1018fc15b4a8e56f552d79366a3c79c0d",
  "0b0ecbb5c3dfefe897f38d1880fca4a81e20603967875da673ba325d3e51116e",
  "717f4baeb6ee9a8858045de74e7db96484b5baf9691f6b447efb13fa7db8ba11"
]
```
This created six new blocks that depend on node-0's transaction to node-4, therefore confirming the transaction. This can be see by viewing node-4's new balance:
```
bellmj@node-4:~$ bitcoin-cli -regtest getbalance
1010.00000000
```
Notice that exactly the amount node-0 sent is added to the account, because all transaction fees are paid by the sending party. \

Now what happened of the fee that node-0 paid? This fee is supposed to be paid to the miners who confirmed the transaction. However, a check of node-1's balance shows the fee not in the wallet:
```
bellmj@node-1:~$ bitcoin-cli -regtest getbalance
0.00000000
```
This is because the bitcoins award for confirming transactions must be confirmed by the block chain. This avoids funds being erroneously awarded in the case of a fork in the blockchain. For this miners fee to be awarded 100 new blocks must confirm the miners work confirming the transactions. After generating 100 new blocks with node-2:
```
bellmj@node-2:~$ bitcoin-cli -regtest generate 100
[
  "57a7f03cb98083ce3dd573cbad0819437c481675dc307661093b9976eab9135f",
  ...
  [98 entries omitted for brevity]
  ...
  "3416130c997b548c519bd4753d6e17b77af9ad46fee8b93826d2904a1eada1c7"
]
```
The miners fee should have been awarded to node-1. We can confirm this by checking node-1's balance:
```
bellmj@node-1:~$ bitcoin-cli -regtest getbalance
1300.00003840
```
We can see an extra 1300 bitcoin in the wallet, this is from the 50 bitcoin award per block successfully added to the chain, this award is also confirmed after 100 new blocks have been added. We can check the details of the award transaction by running the following:
```
bellmj@node-1:~$ bitcoin-cli -regtest listunspent
...
{
  "txid": "746c76f4040d291090f069f1382bd375328b61b587a5a4adf6c04a05af865d66",
  "vout": 0,
  "address": "n4b3SBUsDHvWWv4naRNAAW4v3sX7YXJ5f9",
  "scriptPubKey": "210356bfd32b1148c15f092385581dfb4be62dc7bc6c962879891351934aa35e81eeac",
  "amount": 50.00003840,
  "confirmations": 106,
  "spendable": true,
  "solvable": true,
  "safe": true
},
...
```
#### How the block chain achieved consensus
b.
How did the block chain reach consensus? Describe the steps in detail and give node numbers if needed.
