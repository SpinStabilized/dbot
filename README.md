<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- [![Contributors][contributors-shield]][contributors-url] -->
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/SpinStabilized/dbot">
    <img src="resources/d20.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">DBot</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <!--<br />
    <a href="https://github.com/SpinStabilized/dbot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/SpinStabilized/dbot">View Demo</a> -->
    ·
    <a href="https://github.com/SpinStabilized/dbot/issues">Report Bug</a>
    ·
    <a href="https://github.com/SpinStabilized/dbot/issues">Request Feature</a>
  </p>
</p>


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

[![DBot Screenshot][product-screenshot]](https://github.com/SpinStabilized/dbot)

Another discord bot build for fun. Originally intended as a Dice Rolling bot but I keep adding fun features because I am enjoying the project. The current capabilities of the bot are:

* Dice rolling
* Board Game Geek Hot List & User Information Lookup
* Cowsay
* Fortune

Some features I am considering for the future include:

* Get the latest images from the Curiosity or Perserverance Rovers
* View upcoming space launches

### Built With

* [discordpy](https://discordpy.readthedocs.io/en/latest/index.html)
* [BGG API](https://boardgamegeek.com/wiki/page/BGG_XML_API2)


<!-- GETTING STARTED -->
## Getting Started

To get up and running with DBot:

### Prerequisites

The only pre-requisits to get up and running are Python 3 with `pipenv`. While `pipenv` is not required it makes installation of packages for the project trivial.

* Python 3
  This is highly system dependent. On Windows I recommend using [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) or [Chocolatey](https://chocolatey.org/) and on OS X I can *highly* recommend [Homebrew](https://brew.sh/).
* `pipenv`
  ```sh
  pip install --user pipenv
  ```

Additionally, the project is built with containers in mind so you can install [Docker](https://www.docker.com/products) on your system but the project can be run without being in a container as well.

### Installation

1. Check out [this tutorial on realpython.com](https://realpython.com/how-to-make-a-discord-bot-python/) for recommendations on setting up a [Discord Developer](https://discord.com/developers/docs/intro) account for a bot and getting an API token.
2. Clone the repo
   ```sh
   git clone https://github.com/SpinStabilized/dbot.git
   ```
3. The development environment uses [`pipenv`](https://pipenv.pypa.io/en/latest/#install-pipenv-today). To install a test environment
   ```sh
   pipenv install
   ```
5. Create a `.env` file 
   ```sh
   touch .env
   ```
   Populate the file with the follow information
   ```sh
   DISCORD_TOKEN=your_token_here
   DISCORD_BOT_PREFIX=your_prefix_char_here
   DISCORD_BOT_DEVELOPERS=semicolon_seperated_developer_id_list
   ```
4. To execute the bot in the `pipenv` environment you can execute it directly
   ```sh
   pipenv run src/dbot.py
   ```
   or jump into a shell in the `pipenv` environment and run it with Python
   ```sh
   pipenv shell
   python src/dbot.py
   ```
5. The [Docker](https://www.docker.com/products) compose files can build a container environment that will immediately connect and start running
```sh
docker-compose -f "docker-compose.yml" up -d --build
```
6. If you are using Docker and add any modules with `pipenv install`, make sure you freeze the environment before you run the Docker compose. If you are in a *nix shell (Linux, WSL, OS X) there is a convinience script included
```sh
./freeze.sh
```
7. I develop in [VS Code](https://code.visualstudio.com/) and mostly on a Windows machine. Some of the extensions I find very useful (and should be largly cross-compatible) are
  * [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  * [Git History](https://marketplace.visualstudio.com/items?itemName=donjayamanne.githistory)
  * [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)


<!-- USAGE EXAMPLES -->
## Usage

<!-- Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_ -->

*TBD*


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/SpinStabilized/dbot/issues) for a list of proposed features (and known issues).


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Your Name - [@bjmclaughlin](https://twitter.com/bjmclaughlin) - bjmclauglin@gmail.com

Project Link: [https://github.com/SpinStabilized/dbot](https://github.com/SpinStabilized/dbot)


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [discordpy](https://discordpy.readthedocs.io/en/latest/index.html)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* Numerous bot examples.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- [contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/SpinStabilized/dbot/graphs/contributors -->
[forks-shield]: https://img.shields.io/github/forks/SpinStabilized/dbot?style=for-the-badge
[forks-url]: https://github.com/SpinStabilized/dbot/network/members
[stars-shield]: https://img.shields.io/github/stars/SpinStabilized/dbot?style=for-the-badge
[stars-url]:https://github.com/SpinStabilized/dbot/stargazers
[issues-shield]:https://img.shields.io/github/issues/SpinStabilized/dbot?style=for-the-badge
[issues-url]: https://github.com/SpinStabilized/dbot/issues
[license-shield]: https://img.shields.io/github/license/SpinStabilized/dbot?style=for-the-badge
[license-url]: https://github.com/SpinStabilized/dbot/blob/main/LICENSE
<!-- [linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew -->
[product-screenshot]: resources/dbot_screenshot.png
