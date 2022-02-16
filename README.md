# macpro-platform-doc-conversion ![Build](https://github.com/CMSgov/macpro-platform-doc-conversion/workflows/Deploy/badge.svg?branch=master) [![Maintainability](https://api.codeclimate.com/v1/badges/c6b3d112f68f9be7f95a/maintainability)](https://codeclimate.com/github/CMSgov/macpro-platform-doc-conversion/maintainability) [![CodeQL](https://github.com/CMSgov/macpro-platform-doc-conversion/actions/workflows/codeql-analysis.yml/badge.svg?branch=master)](https://github.com/CMSgov/macpro-platform-doc-conversion/actions/workflows/codeql-analysis.yml) [![Dependabot](https://badgen.net/badge/Dependabot/enabled/green?icon=dependabot)](https://dependabot.com/) [![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier) [![Test Coverage](https://api.codeclimate.com/v1/badges/c6b3d112f68f9be7f95a/test_coverage)](https://codeclimate.com/github/CMSgov/macpro-platform-doc-conversion/test_coverage)

MACPRO Platform document conversion APIs.

Initial API:

- 508 compliant HTML -> 508 compliant PDF (via Prince XML)
  - Input needs to be base 64 encoded
  - Output is base 64 encoded

## Release

Our product is promoted through branches. Master is merged to val to affect a master release, and val is merged to production to affect a production release. Please use the buttons below to promote/release code to higher environments.<br />

| branch     | status                                                                                                               | release                                                                                                                                                                                                                                                     |
| ---------- | -------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| master     | ![master](https://github.com/CMSgov/macpro-platform-doc-conversion/workflows/Deploy/badge.svg?branch=master)         | [![release to master](https://img.shields.io/badge/-Create%20PR-blue.svg)](https://github.com/CMSgov/macpro-platform-doc-conversion/compare?quick_pull=1)                                                                                                   |
| val        | ![val](https://github.com/CMSgov/macpro-platform-doc-conversion/workflows/Deploy/badge.svg?branch=val)               | [![release to val](https://img.shields.io/badge/-Create%20PR-blue.svg)](https://github.com/CMSgov/macpro-platform-doc-conversion/compare/val...master?quick_pull=1&template=PULL_REQUEST_TEMPLATE.val.md&title=Release%20to%20Val)                          |
| production | ![production](https://github.com/CMSgov/macpro-platform-doc-conversion/workflows/Deploy/badge.svg?branch=production) | [![release to production](https://img.shields.io/badge/-Create%20PR-blue.svg)](https://github.com/CMSgov/macpro-platform-doc-conversion/compare/production...val?quick_pull=1&template=PULL_REQUEST_TEMPLATE.production.md&title=Release%20to%20Production) |

## Architecture

![Architecture Diagram](./.images/architecture.svg?raw=true)

## Usage

See master build [here](https://github.com/CMSgov/macpro-platform-doc-conversion/actions?query=branch%3Amaster)

This application is built and deployed via GitHub Actions.

Want to deploy from your Mac?

- Create an AWS account
- Install/configure the AWS CLI
- brew install yarn
- sh deploy.sh

## Requirements

Node - we enforce using a specific version of node, specified in the file `.nvmrc`. This version matches the Lambda runtime. We recommend managing node versions using [NVM](https://github.com/nvm-sh/nvm#installing-and-updating).

Serverless - Get help installing it here: [Serverless Getting Started page](https://www.serverless.com/framework/docs/providers/aws/guide/installation/)

Yarn - in order to install dependencies, you need to [install yarn](https://classic.yarnpkg.com/en/docs/install/).

AWS Account: You'll need an AWS account with appropriate IAM permissions (admin recommended) to deploy this app in Amazon.

If you are on a Mac, you should be able to install all the dependencies like so:

```
# install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash

# select the version specified in .nvmrc
nvm install
nvm use

# install yarn
brew install yarn
```

If you'd like to test deploying prior to committing, you can deploy to AWS as follows:

```
./deploy.sh <branch name>

# Quick and dirty test where "test.hmtl" is a valid html file that is already 508 compliant.
# First we base64 encode the html:
# base64 -i ~/Desktop/test.html -o test_b64.html

# Note output will be a little garbled since we're filtering out special chars
# To properly validate the output perform these steps in JS or Python and decode the API response from base64
# API ID will be output from the deploy
curl -F "data=~@~/Desktop/test_b64.html" --tlsv1.2 https://<API ID>.execute-api.us-east-1.amazonaws.com/<branch name>/prince | sed 's/^"//; s/"$//' | base64 -d > ~/Desktop/test.pdf

# to clean up
./destroy.sh <branch name>
```

## Example Calling the API

To run the Python example calling your deployed API:

```
# Setting up a Python virtualenv is beyond the scope of this guide.
# Below assumes Python 3.8 and a pyenv virtual environment dedicated for calling this API
pyenv activate my-prince-virtual-env
pip install -r examples/python/requirements.txt
python examples/python/call_prince.py https://abc123.execute-api.us-east-1.amazonaws.com/master/prince ~/Desktop
508 html being converted to pdf:

<html lang="en">
        <head>
...
        </body>
      </html>

sending request to https://abc123.execute-api.us-east-1.amazonaws.com/master/prince:
<bound method Response.json of <Response [200]>>
508 PDF written to: /Users/jeffreysobchak/Desktop/prince-master.pdf
```

## Contributing / To-Do

See current open [issues](https://github.com/CMSgov/macpro-platorm-doc-conversion/issues) or check out the [project board](https://github.com/CMSgov/macpro-platform-doc-conversion/projects/1).

Please feel free to open new issues for defects or enhancements.

To contribute:

- Fork this repository
- Make changes in your fork
- Open a pull request targetting this repository

Pull requests are being accepted.

## License

[![License](https://img.shields.io/badge/License-CC0--1.0--Universal-blue.svg)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)

See [LICENSE](LICENSE.md) for full details.

```text
As a work of the United States Government, this project is
in the public domain within the United States.

Additionally, we waive copyright and related rights in the
work worldwide through the CC0 1.0 Universal public domain dedication.
```

## Slack channel

To enable slack integration, set a value for SLACK_WEBHOOK_URL in github actions secret.

To set the SLACK_WEBHOOK_URL:

- Go to https://api.slack.com/apps
- Create new app : fill in the information
- Add features and funtionality----Incoming webhooks--- activative incoming webooks--- Add new webhook to workspace.
- copy new webhook url and set it as SLACK_WEBHOOK_URL in Github Actions Secrets.
