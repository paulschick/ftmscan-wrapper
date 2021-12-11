# ftmscan Client

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Forked from [etherscan python wrapper](https://github.com/corpetty/py-etherscan-api)

## Summary

This was forked from the python client for etherscan. I modified the original
repository for a project that I'm working on. Some of the methods were left
out, so this is not a complete wrapper.

- [ftmscan API documentation](https://ftmscan.com/apis)
- [Create a free API key](https://ftmscan.com/myaccount)


## Usage Instructions

- Add your wallet address to `config.json`.
You may also add a contract address to this in order to
use the `Contracts` class without passing an additional address
during class instantiation
- Create a `.env` file with your ftmscan api key

