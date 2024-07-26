<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/thomasmichaelkane/ao_cropper">
    <img src="docs/images/ao_cropper.gif" alt="Logo" width="200">
  </a>

<h3 align="center">ao_cropper</h3>

  <p align="center">
    Easily crop subsections from AOSLO images with auto-scaling
    <br />
    <a href="https://github.com/thomasmichaelkane/ao_cropper"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/thomasmichaelkane/ao_cropper/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/thomasmichaelkane/ao_cropper/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
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
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#scripts">Scripts</a></li>
        <li><a href="#api">API</a></li>
      </ul>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

In recent years deep learning has allowed for accurate cell detection in high quality AOSLO images of the retina. This has moved the bottleneck of the image analysis for the purpose of cone counting to the laborious task of manually cropping and scaling several sections of very large images. Slow responding of large photoshop documents can slow down the process even further.

This project aims to drastically speed up this manual task by allowing the user to select an unlimited number of scaled crops with a simple double click. Maps-style zoom functionality allows easy navigation of large images, and several other features are available to user which greatly improve the process. The software can only operate on single layer image files, so some use of photoshop for layer selection beforehand is necessary.

#### Features

- Initial input of scaling factors will automatically scale all relevant measurements.
- Retinal centre is placed with a double click and all coordinates are in relation to this point. A scaled scrosshair will show eccentric rings or tick marks.
- An unlimited number of scaled square crop boxes can be placed, updated, and deleted.
- A single image is used for crop placement, however images can be cropped after at the same locations from multiple modalities such as confocal and split inmages.
- Outputs include; labelled crop tifs of the original image at the selected locations, The original image with selected crop locations shown (also in multiple modalities), and csv files containing metadata (coordinates in microns, degrees, etc.). 


<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [![Python][Python.py]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.


### Installation

1. Clone the repo at the desired location
   ```sh
   git clone https://github.com/thomasmichaelkane/ao_cropper.git
   cd ao_cropper
   ```
2. Create a virtual environment
   ```sh
   python -m venv .venv
   ```
2. Activate environment
  <small>Windows</small>
   ```sh
   .venv/Scripts/activate.ps1  
   ```
   <small>Mac/Linux</small>
   ```sh
   source .venv/bin/activate
   ```
3. Install prerequisites
   ```sh
   python -m pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Coming soon :)

## Scripts

Coming soon :)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

## API

Coming soon :)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Thomas Kane - thomas.kane.ucl@gmail.com

Me: https://thomasmichaelkane.github.io/me/

Project Link: [https://github.com/thomasmichaelkane/ao_cropper](https://github.com/thomasmichaelkane/ao_cropper)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[Python.py]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/