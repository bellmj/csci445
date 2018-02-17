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

In order for this transaction to be confirmed we need confirmations by the network. 

b.
How did the block chain reach consensus? Describe the steps in detail and give node numbers if needed.
