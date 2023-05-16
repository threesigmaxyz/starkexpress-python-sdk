# StarkExpress Python SDK [![Github Actions][gha-badge]][gha] [![License: MIT][license-badge]][license]

[gha]: https://github.com/threesigmaxyz/starkexpress-python-sdk/actions
[gha-badge]: https://github.com/threesigmaxyz/starkexpress-python-sdk/actions/workflows/main.yml/badge.svg
[license]: https://opensource.org/licenses/MIT
[license-badge]: https://img.shields.io/badge/License-MIT-blue.svg

**Disclaimer:** This SDK is currently under active development, please [open an issue](https://github.com/threesigmaxyz/starkexpress-python-sdk/issues/new) for bug reporting.

## Introduction
The StarkExpress Python SDK is a collection of tools that allow you to interact with the StarkExpress platform. The SDK is composed of two main components: the StarkExpress Python SDK and the StarkExpress CLI tool.

## Documentation
You can consult the documentation page [here](https://docs.starkexpress.io/reference/cli-tool-reference). We encourage all users to read through the documentation to gain a better understanding of the SDKs and how to use them. Additionally, we welcome any contributions to the documentation.

## Installation
To install the StarkExpress Python SDK and CLI tool, you can use pip package manager. Open your terminal and run the following command:
```bash
pip install git+https://github.com/threesigmaxyz/starkexpress-python-sdk.git
```
This command will download and install the latest SDK version along with its dependencies.

Once the installation is complete, you can verify that the installation was successful by running the following command:
```bash
starkexpress-cli --version
```
If the installation was successful, this command will display the current version of the StarkExpress CLI tool.

## Getting Started
Once you have completed the installation steps, you can get started with the StarkExpress CLI tool.
The following command will display all available commands along with a brief description:
```bash
starkexpress-cli --help
```
Before using the CLI you must authenticate your client with StarkExpress using the provided client ID and secret:
```bash
starkexpress-cli auth login --client-id=CLIENT_ID --client-secret=CLIENT_SECRET
```
More details regarding available commands can be found in the [documentation](https://docs.starkexpress.io/reference/cli-tool-reference).

## About Us
[Three Sigma](https://threesigma.xyz/) is a venture builder firm focused on blockchain engineering, research, and investment. Our mission is to advance the adoption of blockchain technology and contribute towards the healthy development of the Web3 space.

If you are interested in joining our team, please contact us [here](mailto:info@threesigma.xyz).

---

<p align="center">
    <a href="https://threesigma.xyz" target="_blank">
        <img src="https://threesigma.xyz/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fthree-sigma-labs-research-capital-white.0f8e8f50.png&w=2048&q=75" width="75%" />
    </a>
</p>